#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


def transcribe(audio_path: str, language: str) -> str:
    cmd = [
        'python3',
        '/home/andy/.openclaw/workspace/skills/voice-note-dialogue/scripts/groq_transcribe.py',
        audio_path,
        '--language',
        language,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr or res.stdout)
    return res.stdout.strip()


def simple_reply(user_text: str) -> str:
    text = user_text.strip()
    if not text:
        return '老爸，我這邊沒聽清楚，再丟一次給我。'
    if '聽到嗎' in text or '听到吗' in text:
        return '有，我聽得到，老爸 😎'
    return f'我收到你的語音了，重點是：{text}'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('audio')
    p.add_argument('--language', default='zh')
    p.add_argument('--mode', choices=['text', 'tts-handoff'], default='text')
    p.add_argument('--tts-output', help='Path to save reply text for downstream TTS')
    args = p.parse_args()

    transcript = transcribe(args.audio, args.language)
    reply = simple_reply(transcript)

    out = {
        'mode': args.mode,
        'transcription': transcript,
        'reply': reply,
    }

    if args.mode == 'tts-handoff':
        target = Path(args.tts_output or './reply_for_tts.txt')
        target.write_text(reply, encoding='utf-8')
        out['tts_handoff'] = str(target)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
