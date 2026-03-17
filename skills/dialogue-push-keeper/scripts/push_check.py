#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

STATE_PATH = Path('/home/andy/.openclaw/workspace/memory/push-check-state.json')
REPO = '/home/andy/.openclaw/workspace'
BRANCH = 'main'
REMOTE = 'origin'


def git(*args):
    res = subprocess.run(['git', '-C', REPO, *args], capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr or res.stdout)
    return res.stdout.strip()


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding='utf-8'))
    return {}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--write-state', action='store_true')
    args = p.parse_args()

    git('fetch', REMOTE)
    local = git('rev-parse', BRANCH)
    upstream = git('rev-parse', f'{REMOTE}/{BRANCH}')
    ahead = local != upstream and git('rev-list', '--left-right', '--count', f'{REMOTE}/{BRANCH}...{BRANCH}')
    now = datetime.now()
    boundary = now.strftime('%Y-%m-%d %H:') + ('00' if now.minute < 30 else '30')
    minute_ok = now.minute in (0, 30)
    state = load_state()
    last_boundary = state.get('lastBoundary')
    due = minute_ok and boundary != last_boundary
    result = {
        'now': now.strftime('%Y-%m-%d %H:%M'),
        'boundary': boundary,
        'minute_ok': minute_ok,
        'due': due,
        'ahead': bool(ahead and local != upstream),
        'local': local,
        'upstream': upstream,
    }
    if args.write_state and due:
        state['lastBoundary'] = boundary
        save_state(state)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
