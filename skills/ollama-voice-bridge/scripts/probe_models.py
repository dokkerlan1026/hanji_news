#!/usr/bin/env python3
import argparse
import json
import os
import urllib.request

DEFAULT_BASE_URL = os.environ.get('OLLAMA_VOICE_BASE_URL', 'http://127.0.0.1:11434')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', default=DEFAULT_BASE_URL)
    args = p.parse_args()

    with urllib.request.urlopen(f"{args.base_url}/api/tags", timeout=60) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    models = data.get('models', [])
    print(f"Server: {args.base_url}")
    print(f"Models: {len(models)}")
    for m in models:
        print(f"- {m.get('name')}")


if __name__ == '__main__':
    main()
