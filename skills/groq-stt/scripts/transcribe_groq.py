#!/usr/bin/env python3
import argparse
import os
import subprocess
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('audio_file')
    ap.add_argument('--api-key', default=os.environ.get('GROQ_API_KEY'))
    ap.add_argument('--model', default='whisper-large-v3')
    ap.add_argument('--language', default=None)
    ap.add_argument('--prompt', default=None)
    ap.add_argument('--temperature', default='0')
    ap.add_argument('--response-format', default='verbose_json', choices=['json', 'verbose_json', 'text'])
    args = ap.parse_args()

    if not args.api_key:
        raise SystemExit('Missing Groq API key. Pass --api-key or set GROQ_API_KEY.')

    audio = Path(args.audio_file)
    if not audio.exists():
        raise SystemExit(f'Audio file not found: {audio}')

    cmd = [
        'curl', 'https://api.groq.com/openai/v1/audio/transcriptions',
        '-H', f'Authorization: Bearer {args.api_key}',
        '-F', f'model={args.model}',
        '-F', f'file=@{audio}',
        '-F', f'temperature={args.temperature}',
        '-F', f'response_format={args.response_format}',
        '-X', 'POST',
    ]

    if args.language:
        cmd.extend(['-F', f'language={args.language}'])
    if args.prompt:
        cmd.extend(['-F', f'prompt={args.prompt}'])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip())
        raise SystemExit(result.returncode)

    print(result.stdout)


if __name__ == '__main__':
    main()
