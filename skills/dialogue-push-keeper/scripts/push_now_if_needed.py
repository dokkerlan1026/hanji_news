#!/usr/bin/env python3
import json
import subprocess

REPO = '/home/andy/.openclaw/workspace'
BRANCH = 'main'
REMOTE = 'origin'


def git(*args):
    res = subprocess.run(['git', '-C', REPO, *args], capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr or res.stdout)
    return res.stdout.strip()


def main():
    git('fetch', REMOTE)
    counts = git('rev-list', '--left-right', '--count', f'{REMOTE}/{BRANCH}...{BRANCH}')
    behind, ahead = [int(x) for x in counts.split()]
    if ahead <= 0:
        print(json.dumps({'pushed': False, 'reason': 'no-new-commits'}, ensure_ascii=False, indent=2))
        return
    before = git('rev-parse', BRANCH)
    push_out = git('push', REMOTE, BRANCH)
    print(json.dumps({'pushed': True, 'commit': before, 'ahead_count': ahead, 'remote': f'{REMOTE}/{BRANCH}', 'output': push_out}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
