#!/usr/bin/env python3
import argparse
import json
import math
import statistics
import sys
import urllib.parse
import urllib.request

BASE = "https://data-api.binance.vision"
STABLE_PREFIXES = {
    "USDC", "FDUSD", "BUSD", "USDE", "USDS", "DAI", "TUSD", "USDP", "RLUSD", "USD1", "U", "BFUSD", "XUSD"
}
STABLE_SUFFIXES = {"USDT"}
EXCLUDE_SYMBOLS = {
    "USDCUSDT", "FDUSDUSDT", "BUSDUSDT", "USDEUSDT", "TUSDUSDT", "USDPUSDT", "RLUSDUSDT", "USD1USDT", "BFUSDUSDT", "XUSDUSDT", "UUSDT"
}


def get_json(path, params=None):
    if params:
        path = f"{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(BASE + path, timeout=20) as r:
        return json.loads(r.read().decode())


def rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, period + 1):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    for i in range(period + 1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gain = max(diff, 0.0)
        loss = max(-diff, 0.0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def is_excluded(symbol):
    if symbol in EXCLUDE_SYMBOLS:
        return True
    if not symbol.endswith("USDT"):
        return True
    base = symbol[:-4]
    return base in STABLE_PREFIXES


def score_symbol(t):
    symbol = t["symbol"]
    last = float(t["lastPrice"])
    high = float(t["highPrice"])
    low = float(t["lowPrice"])
    change = float(t["priceChangePercent"])
    qv = float(t["quoteVolume"])
    trades = int(t.get("count", 0))
    if last <= 0 or high <= 0 or qv <= 0:
        return None
    distance_high = max(0.0, ((high - last) / high) * 100)
    intraday_range = ((high - low) / low) * 100 if low > 0 else 0.0
    try:
        klines = get_json("/api/v3/klines", {"symbol": symbol, "interval": "1h", "limit": 80})
        closes = [float(k[4]) for k in klines]
    except Exception:
        closes = []
    rsi_1h = rsi(closes) if closes else None
    recent_return = None
    if len(closes) >= 7:
        recent_return = ((closes[-1] - closes[-7]) / closes[-7]) * 100 if closes[-7] else None

    score = 0
    notes = []
    cautions = []

    if qv >= 100_000_000:
        score += 3; notes.append("huge volume")
    elif qv >= 20_000_000:
        score += 2; notes.append("strong volume")
    elif qv >= 5_000_000:
        score += 1; notes.append("acceptable volume")
    else:
        cautions.append("thin volume")

    if 8 <= change <= 35:
        score += 3; notes.append("healthy momentum")
    elif 35 < change <= 60:
        score += 2; notes.append("aggressive move")
    elif 5 <= change < 8:
        score += 1; notes.append("early strength")
    elif change > 60:
        cautions.append("possibly overextended")
    else:
        cautions.append("weak 24h momentum")

    if distance_high <= 1.5:
        score += 2; notes.append("near 24h high")
    elif distance_high <= 3:
        score += 1; notes.append("holding near highs")
    else:
        cautions.append("far from 24h high")

    if rsi_1h is not None:
        if 58 <= rsi_1h <= 72:
            score += 2; notes.append("RSI constructive")
        elif 72 < rsi_1h <= 80:
            score += 1; notes.append("RSI strong")
            cautions.append("RSI hot")
        elif rsi_1h > 80:
            cautions.append("RSI extreme")
        elif 50 <= rsi_1h < 58:
            score += 1; notes.append("RSI improving")
        else:
            cautions.append("RSI weak")
    else:
        cautions.append("missing RSI")

    if recent_return is not None:
        if recent_return > 2:
            score += 1; notes.append("recent hourly follow-through")
        elif recent_return < -2:
            cautions.append("recent hourly fade")

    if intraday_range > 45 and qv < 20_000_000:
        cautions.append("wide range with suspect quality")
    if trades < 3000 and qv < 10_000_000:
        cautions.append("low trade count")

    rating = "watch"
    if score >= 8 and "thin volume" not in cautions and "RSI extreme" not in cautions:
        rating = "candidate"
    elif score < 6:
        rating = "pass"

    return {
        "symbol": symbol,
        "price": last,
        "change_24h_pct": change,
        "quote_volume": qv,
        "distance_to_high_pct": distance_high,
        "intraday_range_pct": intraday_range,
        "trade_count": trades,
        "rsi_1h": None if rsi_1h is None else round(rsi_1h, 2),
        "recent_6h_return_pct": None if recent_return is None else round(recent_return, 2),
        "score": score,
        "rating": rating,
        "notes": notes,
        "cautions": cautions,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=6)
    ap.add_argument("--min-volume", type=float, default=5_000_000)
    ap.add_argument("--min-change", type=float, default=6.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    tickers = get_json("/api/v3/ticker/24hr")
    rows = []
    for t in tickers:
        symbol = t.get("symbol", "")
        if is_excluded(symbol):
            continue
        try:
            qv = float(t["quoteVolume"])
            change = float(t["priceChangePercent"])
        except Exception:
            continue
        if qv < args.min_volume or change < args.min_change:
            continue
        scored = score_symbol(t)
        if scored:
            rows.append(scored)
    rows.sort(key=lambda x: (x["rating"] == "candidate", x["score"], x["quote_volume"], x["change_24h_pct"]), reverse=True)
    rows = rows[: args.limit]

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return

    real = [r for r in rows if r["rating"] in {"candidate", "watch"}]
    if not real:
        print("NO_SIGNAL")
        return

    for i, r in enumerate(real, 1):
        print(f"{i}. {r['symbol']} | rating={r['rating']} | score={r['score']}")
        print(f"   24h={r['change_24h_pct']:.2f}% | vol=${r['quote_volume']:,.0f} | dist_high={r['distance_to_high_pct']:.2f}% | RSI1h={r['rsi_1h']}")
        print(f"   why: {', '.join(r['notes']) if r['notes'] else 'n/a'}")
        if r['cautions']:
            print(f"   caution: {', '.join(r['cautions'])}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
