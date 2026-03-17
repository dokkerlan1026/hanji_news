#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

EDGE_TTS_BIN = '/home/andy/.npm-global/lib/node_modules/openclaw/node_modules/.bin/node-edge-tts'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--text', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--voice', default='zh-TW-HsiaoYuNeural')
    p.add_argument('--lang', default='zh-TW')
    p.add_argument('--rate', default='default')
    args = p.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        EDGE_TTS_BIN,
        '--text', args.text,
        '--filepath', str(out),
        '--voice', args.voice,
        '--lang', args.lang,
        '--rate', args.rate,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr or res.stdout)
    print(str(out))


if __name__ == '__main__':
    main()
