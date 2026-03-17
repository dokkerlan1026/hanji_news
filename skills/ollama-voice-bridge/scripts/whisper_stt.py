#!/usr/bin/env python3
import argparse
import base64
import json
from pathlib import Path
import urllib.request


def call_generate(base_url, model, prompt, system=None):
    payload = {'model': model, 'prompt': prompt, 'stream': False}
    if system:
        payload['system'] = system
    req = urllib.request.Request(
        f"{base_url}/api/generate",
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode('utf-8'))


def build_audio_prompt(audio_path, language):
    p = Path(audio_path)
    raw = p.read_bytes()
    b64 = base64.b64encode(raw).decode('ascii')
    return (
        '你是語音轉文字模型。\n'
        f'目標語言：{language or "auto"}\n'
        f'檔名：{p.name}\n'
        f'副檔名：{p.suffix}\n'
        f'大小：{len(raw)} bytes\n'
        '以下是音訊檔案的 base64 內容。若模型支援，請盡可能逐字轉錄，只輸出轉錄文字；若不支援，請直接回答 UNSUPPORTED_AUDIO_INPUT。\n\n'
        f'{b64}'
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', default='http://220.132.50.141:11434')
    p.add_argument('--model', default='karanchopda333/whisper:latest')
    p.add_argument('--language', default='zh')
    p.add_argument('--text', help='Prompt-driven STT test input')
    p.add_argument('--audio', help='Audio file path for best-effort base64 prompt')
    p.add_argument('--output')
    args = p.parse_args()

    if not args.text and not args.audio:
        raise SystemExit('Provide --text or --audio')

    if args.text:
        prompt = f'請逐字轉錄：{args.text}。只輸出轉錄文字。'
    else:
        prompt = build_audio_prompt(args.audio, args.language)

    data = call_generate(args.base_url, args.model, prompt)
    text = (data.get('response') or '').strip()
    if args.output:
        Path(args.output).write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
