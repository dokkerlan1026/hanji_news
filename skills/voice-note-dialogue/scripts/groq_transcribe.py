#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path


def load_key_from_bashrc() -> str:
    bashrc = Path.home() / '.bashrc'
    text = bashrc.read_text(encoding='utf-8') if bashrc.exists() else ''
    m = re.search(r"export\s+GROQ_API_KEY='([^']+)'", text)
    if not m:
        raise SystemExit('Missing GROQ_API_KEY in ~/.bashrc')
    return m.group(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('audio')
    p.add_argument('--language', default='zh')
    args = p.parse_args()

    key = load_key_from_bashrc()
    cmd = [
        'python3',
        '/home/andy/.openclaw/workspace/skills/groq-stt/scripts/transcribe_groq.py',
        args.audio,
        '--language', args.language,
        '--api-key', key,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr or res.stdout)
    raw = res.stdout.strip()
    try:
        data = json.loads(raw)
        print((data.get('text') or '').strip())
    except Exception:
        print(raw)


if __name__ == '__main__':
    main()
