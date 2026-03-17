#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

WORKSPACE = Path('/home/andy/.openclaw/workspace')
YT_DLP = WORKSPACE / '.local/bin/yt-dlp'
FFMPEG = WORKSPACE / '.local/lib/youtube-vision/node_modules/ffmpeg-static/ffmpeg'
FFPROBE = WORKSPACE / '.local/lib/youtube-vision/node_modules/ffprobe-static/bin/linux/x64/ffprobe'
OCR_SCRIPT = WORKSPACE / 'skills/youtube-timeline-vision/scripts/ocr_frames.js'


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def capture(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd, text=True)


def sanitize(name):
    name = re.sub(r'[^a-zA-Z0-9._-]+', '-', name)
    return name.strip('-')[:80] or 'video'


def ts_to_seconds(ts):
    ts = ts.replace(',', '.')
    parts = ts.split(':')
    parts = [float(p) for p in parts]
    if len(parts) == 3:
        h, m, s = parts
        return h * 3600 + m * 60 + s
    if len(parts) == 2:
        m, s = parts
        return m * 60 + s
    return parts[0]


def seconds_to_ts(value):
    value = int(value)
    h = value // 3600
    m = (value % 3600) // 60
    s = value % 60
    if h:
        return f'{h:02d}:{m:02d}:{s:02d}'
    return f'{m:02d}:{s:02d}'


def parse_vtt(path):
    items = []
    if not path.exists():
        return items
    lines = path.read_text(errors='ignore').splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if '-->' in line:
            start, end = [x.strip() for x in line.split('-->')[:2]]
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip():
                txt = re.sub(r'<[^>]+>', '', lines[i]).strip()
                if txt and txt != 'WEBVTT':
                    text_lines.append(txt)
                i += 1
            text = ' '.join(text_lines).strip()
            if text:
                items.append({
                    'start': ts_to_seconds(start.split(' ')[0]),
                    'end': ts_to_seconds(end.split(' ')[0]),
                    'text': text,
                })
        i += 1
    return items


def parse_ffprobe(video_path):
    raw = capture([str(FFPROBE), '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', str(video_path)])
    return json.loads(raw)


def choose_subtitle_langs(info):
    pools = []
    if isinstance(info.get('subtitles'), dict):
        pools.extend(info['subtitles'].keys())
    if isinstance(info.get('automatic_captions'), dict):
        pools.extend(info['automatic_captions'].keys())

    seen = []
    for lang in pools:
        if lang not in seen:
            seen.append(lang)

    preferred_prefixes = ['en', 'zh-Hant', 'zh-Hans', 'zh', 'ja', 'ko', 'de']
    picked = []
    for prefix in preferred_prefixes:
        for lang in seen:
            if lang == prefix or lang.startswith(prefix + '-'):
                if lang not in picked:
                    picked.append(lang)
        if len(picked) >= 3:
            break

    if not picked:
        picked = seen[:2]
    return picked


def merge_timeline(duration, subtitles, ocr_items, sample_every):
    buckets = {}
    for item in subtitles:
        sec = int(item['start'] // sample_every * sample_every)
        buckets.setdefault(sec, {'speech': [], 'visual': []})
        buckets[sec]['speech'].append(item['text'])
    for item in ocr_items:
        sec = item['second']
        if item['text']:
            buckets.setdefault(sec, {'speech': [], 'visual': []})
            buckets[sec]['visual'].append(item['text'])

    out = []
    for sec in sorted(buckets.keys()):
        out.append({
            'start': seconds_to_ts(sec),
            'end': seconds_to_ts(min(sec + sample_every, duration)),
            'speech': ' '.join(dict.fromkeys(buckets[sec]['speech'])).strip(),
            'visual': ' | '.join(dict.fromkeys(buckets[sec]['visual'])).strip(),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--output-dir', default=str(WORKSPACE / 'outputs/youtube-vision'))
    ap.add_argument('--sample-every', type=int, default=10)
    args = ap.parse_args()

    out_root = Path(args.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    info_raw = capture([str(YT_DLP), '--dump-single-json', args.url])
    info = json.loads(info_raw)
    slug = sanitize(info.get('id') or info.get('title') or 'video')
    job_dir = out_root / slug
    frames_dir = job_dir / 'frames'
    job_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    video_path = job_dir / f'{slug}.mp4'
    subtitle_langs = choose_subtitle_langs(info)

    download_cmd = [
        str(YT_DLP), '-f', 'bv*+ba/b',
        '--ffmpeg-location', str(FFMPEG.parent),
        '--write-auto-sub', '--write-sub',
        '--sub-format', 'vtt',
        '-o', str(job_dir / '%(id)s.%(ext)s'),
    ]
    if subtitle_langs:
        download_cmd += ['--sub-langs', ','.join(subtitle_langs)]
    download_cmd += [args.url]
    run(download_cmd)

    candidates = []
    for pattern in ('*.mp4', '*.webm', '*.mkv', '*.mov'):
        candidates.extend(sorted(job_dir.glob(pattern)))
    if not candidates:
        raise SystemExit('No video downloaded')
    downloaded = candidates[0]
    video_path = job_dir / f'{slug}{downloaded.suffix}'
    if downloaded != video_path:
        downloaded.rename(video_path)

    probe = parse_ffprobe(video_path)
    duration = int(float(probe['format']['duration']))

    run([
        str(FFMPEG), '-i', str(video_path), '-vf', f'fps=1/{args.sample_every}',
        str(frames_dir / 'frame_%04d.jpg')
    ])

    ocr_json = job_dir / 'ocr.json'
    try:
        run(['node', str(OCR_SCRIPT), str(frames_dir), str(ocr_json)])
        ocr_items_raw = json.loads(ocr_json.read_text())
    except Exception:
        ocr_items_raw = []
    ocr_items = []
    for idx, item in enumerate(ocr_items_raw):
        ocr_items.append({
            'second': idx * args.sample_every,
            'file': item['file'],
            'text': item.get('text', ''),
        })

    sub_files = list(job_dir.glob('*.vtt'))
    subtitles = []
    for sub in sub_files:
        subtitles.extend(parse_vtt(sub))
    subtitles.sort(key=lambda x: x['start'])

    timeline = merge_timeline(duration, subtitles, ocr_items, args.sample_every)

    summary = {
        'title': info.get('title'),
        'uploader': info.get('uploader'),
        'duration': duration,
        'duration_ts': seconds_to_ts(duration),
        'video_path': str(video_path),
        'frames_dir': str(frames_dir),
        'subtitle_count': len(subtitles),
        'frame_count': len(ocr_items),
        'timeline_count': len(timeline),
    }

    (job_dir / 'info.json').write_text(json.dumps(info, ensure_ascii=False, indent=2))
    (job_dir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    (job_dir / 'subtitles.json').write_text(json.dumps(subtitles, ensure_ascii=False, indent=2))
    (job_dir / 'visual_events.json').write_text(json.dumps(ocr_items, ensure_ascii=False, indent=2))
    (job_dir / 'timeline.json').write_text(json.dumps(timeline, ensure_ascii=False, indent=2))

    md = [
        f"# {info.get('title', slug)}",
        '',
        f"- Uploader: {info.get('uploader', 'unknown')}",
        f"- Duration: {seconds_to_ts(duration)}",
        f"- Subtitle entries: {len(subtitles)}",
        f"- Sampled frames: {len(ocr_items)} (every {args.sample_every}s)",
        '',
        '## Timeline',
        ''
    ]
    for item in timeline[:80]:
        speech = item['speech'] or '—'
        visual = item['visual'] or '—'
        md.append(f"- **{item['start']} - {item['end']}**")
        md.append(f"  - Speech: {speech}")
        md.append(f"  - Visual/OCR: {visual}")
    (job_dir / 'timeline.md').write_text('\n'.join(md))

    print(json.dumps({'ok': True, 'job_dir': str(job_dir), 'summary': summary}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
