#!/usr/bin/env python3
import argparse
from pathlib import Path
from urllib.parse import quote


def upsert_readme(repo_root: Path, date_str: str, md_name: str, summary: str, tags: list[str]):
    readme = repo_root / 'README.md'
    text = readme.read_text(encoding='utf-8') if readme.exists() else '# hanji_news\n\n## 目錄\n'
    folder_link = f"[`{date_str}/`](./{date_str}/)"
    file_link = f"[`{md_name}`](./{date_str}/{quote(md_name)})"
    tag_text = ' '.join(f'`{t}`' for t in tags)
    block = f"\n## {date_str}\n\n資料夾：{folder_link}\n\n- {file_link}\n  - 標籤：{tag_text}\n  - 摘要：{summary}\n"

    if f'## {date_str}' in text:
        if md_name in text:
            return
        marker = f'## {date_str}'
        idx = text.index(marker)
        next_idx = text.find('\n## ', idx + len(marker))
        if next_idx == -1:
            text = text.rstrip() + f"\n- {file_link}\n  - 標籤：{tag_text}\n  - 摘要：{summary}\n"
        else:
            section = text[idx:next_idx]
            section = section.rstrip() + f"\n- {file_link}\n  - 標籤：{tag_text}\n  - 摘要：{summary}\n\n"
            text = text[:idx] + section + text[next_idx:]
    else:
        text = text.rstrip() + '\n' + block
    readme.write_text(text, encoding='utf-8')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo-root', required=True)
    p.add_argument('--date', required=True)
    p.add_argument('--time-prefix', required=True)
    p.add_argument('--transcription', required=True)
    p.add_argument('--reply', required=True)
    p.add_argument('--audio-output')
    p.add_argument('--title', default='語音留言測試')
    args = p.parse_args()

    repo_root = Path(args.repo_root)
    day_dir = repo_root / args.date
    day_dir.mkdir(parents=True, exist_ok=True)

    md_name = f"{args.time_prefix}_{args.title}.md"
    md_path = day_dir / md_name

    lines = [
        f"# {args.title}",
        '',
        f"- 日期：{args.date}",
        f"- 時間：{args.time_prefix}",
        f"- 類型：語音留言對話測試",
        '',
        '## 轉錄文字',
        '',
        args.transcription,
        '',
        '## 憨吉回覆',
        '',
        args.reply,
        '',
    ]
    if args.audio_output:
        audio_name = Path(args.audio_output).name
        lines += ['## TTS 音檔', '', f'- [`{audio_name}`](./{quote(audio_name)})', '']
    md_path.write_text('\n'.join(lines), encoding='utf-8')

    summary = '記錄一則語音留言測試，包含語音轉文字結果、憨吉回覆，以及可選的 TTS 音檔。'
    tags = ['語音對話', '測試', 'AI 助手']
    upsert_readme(repo_root, args.date, md_name, summary, tags)
    print(str(md_path))


if __name__ == '__main__':
    main()
