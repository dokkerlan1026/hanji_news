#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request


def post_json(url, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-url', default='http://220.132.50.141:11434')
    ap.add_argument('--model', default='karanchopda333/whisper:latest')
    args = ap.parse_args()

    data = post_json(args.base_url.rstrip('/') + '/api/show', {'name': args.model})
    details = data.get('details', {})
    parent = details.get('parent_model', '')
    family = details.get('family', '')
    modelfile = data.get('modelfile', '')

    looks_text_only = False
    reasons = []
    if parent.startswith('llama'):
        looks_text_only = True
        reasons.append(f'parent_model={parent}')
    if family == 'llama':
        looks_text_only = True
        reasons.append(f'family={family}')
    if 'TEMPLATE' in modelfile and 'Messages' in modelfile:
        looks_text_only = True
        reasons.append('chat-template-present')

    result = {
        'model': args.model,
        'base_url': args.base_url,
        'details': details,
        'looks_text_only': looks_text_only,
        'reasons': reasons,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if looks_text_only:
        sys.exit(2)


if __name__ == '__main__':
    main()
