#!/usr/bin/env python3
import argparse
import hashlib
import hmac
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

PUBLIC_BASE = "https://data-api.binance.vision"
PRIVATE_BASE = "https://api.binance.com"


def read_env_file(path):
    vals = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        vals[k.strip()] = v.strip()
    return vals


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def signed_balances():
    env = read_env_file('/home/andy/.openclaw/credentials/binance.env')
    api_key = env.get('BINANCE_API_KEY')
    api_secret = env.get('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        raise RuntimeError('Missing Binance credentials')
    server_time = get_json(PRIVATE_BASE + '/api/v3/time')['serverTime']
    params = {'timestamp': server_time, 'recvWindow': 5000}
    qs = urllib.parse.urlencode(params)
    sig = hmac.new(api_secret.encode(), qs.encode(), hashlib.sha256).hexdigest()
    url = PRIVATE_BASE + '/api/v3/account?' + qs + '&signature=' + sig
    data = get_json(url, headers={'X-MBX-APIKEY': api_key})
    rows = []
    for b in data.get('balances', []):
        free = float(b.get('free', 0) or 0)
        locked = float(b.get('locked', 0) or 0)
        qty = free + locked
        if qty > 0:
            rows.append({'asset': b['asset'], 'qty': qty})
    return rows


def ticker(symbol):
    url = PUBLIC_BASE + '/api/v3/ticker/24hr?' + urllib.parse.urlencode({'symbol': symbol})
    return get_json(url)


def analyze(asset, qty, min_usdt):
    if asset == 'USDT':
        return None
    symbol = asset + 'USDT'
    try:
        t = ticker(symbol)
    except Exception:
        return None
    last = float(t['lastPrice'])
    change = float(t['priceChangePercent'])
    high = float(t['highPrice'])
    vol = float(t['quoteVolume'])
    value = qty * last
    if value < min_usdt:
        return None
    dist_high = ((high - last) / high) * 100 if high > 0 else 0
    action = 'hold'
    reasons = []
    cautions = []
    if change >= 20 and dist_high > 6:
        action = 'consider-trim'
        reasons.append('large 24h pump already fading from highs')
    elif change >= 12 and dist_high <= 3:
        action = 'watch-for-trim'
        reasons.append('strong gain near highs; protect profit if momentum stalls')
    elif change <= -8:
        action = 'risk-review'
        cautions.append('weak 24h momentum')
    else:
        reasons.append('no strong exit signal yet')
    if vol < 5_000_000:
        cautions.append('lower liquidity')
    return {
        'asset': asset,
        'symbol': symbol,
        'qty': round(qty, 8),
        'price': last,
        'value_usdt': round(value, 4),
        'change_24h_pct': round(change, 2),
        'distance_to_high_pct': round(dist_high, 2),
        'quote_volume': round(vol, 2),
        'action': action,
        'reasons': reasons,
        'cautions': cautions,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min-usdt', type=float, default=5.0)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    rows = []
    for b in signed_balances():
        r = analyze(b['asset'], b['qty'], args.min_usdt)
        if r:
            rows.append(r)
    rows.sort(key=lambda x: x['value_usdt'], reverse=True)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print('NO_SIGNAL')
        return
    meaningful = [r for r in rows if r['action'] != 'hold']
    if not meaningful:
        print('NO_SIGNAL')
        return
    for r in meaningful:
        print(f"{r['asset']} ({r['symbol']}) | action={r['action']} | value=${r['value_usdt']}")
        print(f"  24h={r['change_24h_pct']}% | dist_high={r['distance_to_high_pct']}%")
        print(f"  why: {', '.join(r['reasons'])}")
        if r['cautions']:
            print(f"  caution: {', '.join(r['cautions'])}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)
