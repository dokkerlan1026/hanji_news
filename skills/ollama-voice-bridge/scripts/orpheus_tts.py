#!/usr/bin/env python3
import argparse
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', default='http://220.132.50.141:11434')
    p.add_argument('--model', default='sematre/orpheus:zh')
    p.add_argument('--text', required=True, help='Text to send to the Orpheus model')
    p.add_argument('--style', default='natural', help='Style hint for prompt')
    p.add_argument('--output', help='Path to save raw model response')
    args = p.parse_args()

    prompt = (
        '你是中文語音生成模型。\n'
        f'風格：{args.style}\n'
        '請根據以下文字產生適合語音輸出的內容；如果模型需要特殊格式，請直接輸出原始可用內容，不要加說明。\n\n'
        f'{args.text}'
    )
    data = call_generate(args.base_url, args.model, prompt)
    text = data.get('response', '')
    if args.output:
        Path(args.output).write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
