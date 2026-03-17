#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def run_json(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr or res.stdout)
    return json.loads(res.stdout)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('audio')
    p.add_argument('--date', required=True)
    p.add_argument('--time-prefix', required=True)
    p.add_argument('--repo-root', default='/home/andy/.openclaw/workspace')
    p.add_argument('--title', default='語音留言測試')
    p.add_argument('--with-tts', action='store_true')
    args = p.parse_args()

    flow = run_json([
        'python3', str(SCRIPT_DIR / 'voice_note_flow.py'),
        args.audio,
        '--mode', 'tts-handoff' if args.with_tts else 'text',
        '--tts-output', str(Path(args.repo_root) / 'reply_for_tts.txt'),
    ])

    audio_out = None
    if args.with_tts:
        audio_out = str(Path(args.repo_root) / args.date / f"{args.time_prefix}_語音留言回覆.mp3")
        subprocess.run([
            'python3', str(SCRIPT_DIR / 'edge_tts_synthesize.py'),
            '--text', flow['reply'],
            '--output', audio_out,
        ], check=True, capture_output=True, text=True)

    archive_cmd = [
        'python3', str(SCRIPT_DIR / 'archive_voice_note.py'),
        '--repo-root', args.repo_root,
        '--date', args.date,
        '--time-prefix', args.time_prefix,
        '--transcription', flow['transcription'],
        '--reply', flow['reply'],
        '--title', args.title,
    ]
    if audio_out:
        archive_cmd += ['--audio-output', audio_out]
    res = subprocess.run(archive_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr or res.stdout)

    out = {
        'transcription': flow['transcription'],
        'reply': flow['reply'],
        'archive_markdown': res.stdout.strip(),
    }
    if audio_out:
        out['tts_audio'] = audio_out
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
