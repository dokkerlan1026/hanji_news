#!/usr/bin/env python3
import argparse
import json
import urllib.request


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', default='http://220.132.50.141:11434')
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
