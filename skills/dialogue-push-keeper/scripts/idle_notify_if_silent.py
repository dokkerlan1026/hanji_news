#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)


def latest_user_message_after(transcript_path: Path, since: datetime):
    if not transcript_path.exists():
        return None
    latest = None
    with transcript_path.open('r', encoding='utf-8') as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            ts = obj.get('timestamp')
            msg = obj.get('message') or {}
            if not ts or msg.get('role') != 'user':
                continue
            dt = parse_ts(ts)
            if dt > since:
                latest = dt
    return latest


def send_message(channel: str, target: str, message: str):
    cmd = [
        'openclaw', 'message', 'send',
        '--channel', channel,
        '--target', target,
        '--message', message,
        '--json',
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr or res.stdout)
    print(res.stdout.strip())


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--transcript', required=True)
    p.add_argument('--since', required=True, help='ISO timestamp of assistant reply that started idle timer')
    p.add_argument('--channel', required=True)
    p.add_argument('--target', required=True)
    p.add_argument('--message', required=True)
    args = p.parse_args()

    since = parse_ts(args.since)
    latest = latest_user_message_after(Path(args.transcript), since)
    if latest is not None:
        print(json.dumps({'sent': False, 'reason': 'user-message-after-since', 'latestUserTs': latest.isoformat()}, ensure_ascii=False, indent=2))
        return
    send_message(args.channel, args.target, args.message)


if __name__ == '__main__':
    main()
