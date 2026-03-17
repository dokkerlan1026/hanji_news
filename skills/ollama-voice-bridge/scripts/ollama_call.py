#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.error
import urllib.request


def post_json(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', default='http://220.132.50.141:11434')
    p.add_argument('--endpoint', choices=['generate', 'chat', 'show'], default='generate')
    p.add_argument('--model', required=True)
    p.add_argument('--prompt')
    p.add_argument('--system')
    p.add_argument('--stream', action='store_true')
    p.add_argument('--raw', action='store_true')
    args = p.parse_args()

    if args.endpoint == 'show':
        payload = {'name': args.model}
    elif args.endpoint == 'chat':
        payload = {'model': args.model, 'messages': [{'role': 'user', 'content': args.prompt or ''}], 'stream': False}
        if args.system:
            payload['messages'].insert(0, {'role': 'system', 'content': args.system})
    else:
        payload = {'model': args.model, 'prompt': args.prompt or '', 'stream': False}
        if args.system:
            payload['system'] = args.system

    url = f"{args.base_url}/api/{args.endpoint}"
    try:
        data = post_json(url, payload)
    except urllib.error.HTTPError as e:
        sys.stderr.write(e.read().decode('utf-8', errors='replace'))
        raise

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    if args.endpoint == 'show':
        summary = {
            'model': args.model,
            'capabilities': data.get('capabilities'),
            'details': data.get('details'),
            'parameters': data.get('parameters'),
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    text = data.get('response') or data.get('message', {}).get('content', '')
    print(text)


if __name__ == '__main__':
    main()
