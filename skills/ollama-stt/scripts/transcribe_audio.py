#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path('/home/andy/.openclaw/workspace')
FFMPEG = WORKSPACE / '.local/lib/youtube-vision/node_modules/ffmpeg-static/ffmpeg'
INSPECT = WORKSPACE / 'skills/ollama-stt/scripts/inspect_ollama_model.py'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('audio_file')
    ap.add_argument('--base-url', default='http://220.132.50.141:11434')
    ap.add_argument('--model', default='karanchopda333/whisper:latest')
    ap.add_argument('--output-wav')
    args = ap.parse_args()

    audio = Path(args.audio_file)
    if not audio.exists():
        raise SystemExit(f'Audio file not found: {audio}')

    inspect = subprocess.run([
        'python3', str(INSPECT), '--base-url', args.base_url, '--model', args.model
    ], capture_output=True, text=True)

    if inspect.returncode != 0:
        print(inspect.stdout.strip())
        raise SystemExit(
            'Current Ollama model does not look like a real STT/audio model. '
            'Do not use it for transcription until a genuine speech model or speech API is available.'
        )

    wav_path = Path(args.output_wav) if args.output_wav else audio.with_suffix('.stt-input.wav')
    subprocess.run([
        str(FFMPEG), '-y', '-i', str(audio), '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', str(wav_path)
    ], check=True)

    raise SystemExit(
        'Audio normalized successfully, but Ollama audio transcription is not wired because the current model/API is not a verified speech endpoint yet.'
    )


if __name__ == '__main__':
    main()
