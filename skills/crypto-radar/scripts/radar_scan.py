#!/usr/bin/env python3
import argparse
import json
import math
import subprocess
import sys
import urllib.parse
import urllib.request

BASE = "https://data-api.binance.vision"
STABLE_PREFIXES = {
    "USDC", "FDUSD", "BUSD", "USDE", "USDS", "DAI", "TUSD", "USDP", "RLUSD", "USD1", "U", "BFUSD", "XUSD"
}
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
    gains, losses = [], []
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


def ema(values, period):
    if len(values) < period:
        return None
    k = 2 / (period + 1)
    e = sum(values[:period]) / period
    for v in values[period:]:
        e = v * k + e * (1 - k)
    return e


def macd_signal(closes):
    if len(closes) < 35:
        return None
    ema12_list = []
    ema26_list = []
    e12 = sum(closes[:12]) / 12
    e26 = sum(closes[:26]) / 26
    k12 = 2 / 13
    k26 = 2 / 27
    for i, v in enumerate(closes):
        if i >= 12:
            e12 = v * k12 + e12 * (1 - k12)
            ema12_list.append(e12)
        if i >= 26:
            e26 = v * k26 + e26 * (1 - k26)
            ema26_list.append(e26)
    macd_line = []
    offset = len(ema12_list) - len(ema26_list)
    for i, v in enumerate(ema26_list):
        macd_line.append(ema12_list[i + offset] - v)
    if len(macd_line) < 9:
        return None
    signal = sum(macd_line[:9]) / 9
    k9 = 2 / 10
    for v in macd_line[9:]:
        signal = v * k9 + signal * (1 - k9)
    hist = macd_line[-1] - signal
    prev_hist = macd_line[-2] - signal if len(macd_line) >= 2 else hist
    return {
        "macd": round(macd_line[-1], 6),
        "signal": round(signal, 6),
        "hist": round(hist, 6),
        "bullish": macd_line[-1] > signal,
        "improving": hist > prev_hist,
    }


def is_excluded(symbol):
    if symbol in EXCLUDE_SYMBOLS:
        return True
    if not symbol.endswith("USDT"):
        return True
    return symbol[:-4] in STABLE_PREFIXES


def get_klines(symbol, interval, limit):
    return get_json("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": limit})


def false_breakout_check(klines, last_price, high_24h):
    highs = [float(k[2]) for k in klines]
    closes = [float(k[4]) for k in klines]
    opens = [float(k[1]) for k in klines]
    if len(closes) < 5:
        return {"flag": False, "reasons": []}
    recent_high = max(highs[-6:-1]) if len(highs) >= 6 else max(highs[:-1])
    candle_range = max(float(klines[-1][2]) - float(klines[-1][3]), 1e-9)
    upper_wick = float(klines[-1][2]) - max(float(klines[-1][1]), float(klines[-1][4]))
    wick_ratio = upper_wick / candle_range
    reasons = []
    flag = False
    if float(klines[-1][2]) > recent_high and closes[-1] < recent_high:
        flag = True
        reasons.append("broke above recent high but closed back below")
    if wick_ratio > 0.45 and closes[-1] < opens[-1]:
        flag = True
        reasons.append("long upper wick on latest candle")
    if high_24h > 0 and ((high_24h - last_price) / high_24h) * 100 > 6:
        reasons.append("already faded notably from 24h high")
    return {"flag": flag, "reasons": reasons}


def run_news_check(symbol):
    try:
        out = subprocess.check_output([
            sys.executable,
            "skills/crypto-radar/scripts/news_check.py",
            symbol,
            "--json",
        ], text=True, timeout=25)
        return json.loads(out)
    except Exception:
        return None


def score_symbol(t, with_news=False):
    symbol = t["symbol"]
    last = float(t["lastPrice"])
    high = float(t["highPrice"])
    low = float(t["lowPrice"])
    change = float(t["priceChangePercent"])
    qv = float(t["quoteVolume"])
    trades = int(t.get("count", 0))
    if last <= 0 or high <= 0 or qv <= 0:
        return None

    k15 = get_klines(symbol, "15m", 100)
    k1h = get_klines(symbol, "1h", 100)
    k4h = get_klines(symbol, "4h", 100)
    c15 = [float(k[4]) for k in k15]
    c1h = [float(k[4]) for k in k1h]
    c4h = [float(k[4]) for k in k4h]

    rsi15 = rsi(c15)
    rsi1h = rsi(c1h)
    rsi4h = rsi(c4h)
    macd1h = macd_signal(c1h)
    distance_high = max(0.0, ((high - last) / high) * 100)
    intraday_range = ((high - low) / low) * 100 if low > 0 else 0.0
    recent_6h = ((c1h[-1] - c1h[-7]) / c1h[-7]) * 100 if len(c1h) >= 7 and c1h[-7] else None
    false_break = false_breakout_check(k1h, last, high)

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

    if 8 <= change <= 30:
        score += 3; notes.append("healthy 24h momentum")
    elif 30 < change <= 50:
        score += 2; notes.append("strong move")
    elif 6 <= change < 8:
        score += 1; notes.append("early momentum")
    elif change > 50:
        cautions.append("possibly overextended")
    else:
        cautions.append("weak 24h momentum")

    if distance_high <= 1.5:
        score += 2; notes.append("near 24h high")
    elif distance_high <= 3:
        score += 1; notes.append("holding near highs")
    else:
        cautions.append("far from 24h high")

    rsi_pack = [r for r in [rsi15, rsi1h, rsi4h] if r is not None]
    if rsi1h is not None:
        if 58 <= rsi1h <= 72:
            score += 2; notes.append("1h RSI constructive")
        elif 72 < rsi1h <= 80:
            score += 1; notes.append("1h RSI strong")
            cautions.append("1h RSI hot")
        elif rsi1h > 80:
            cautions.append("1h RSI extreme")
        elif 50 <= rsi1h < 58:
            score += 1; notes.append("1h RSI improving")
        else:
            cautions.append("1h RSI weak")
    if rsi15 and rsi1h and rsi4h and rsi15 > 60 and rsi1h > 58 and rsi4h > 52:
        score += 2; notes.append("multi-timeframe RSI aligned")
    elif rsi15 and rsi1h and rsi15 > 75 and rsi1h < 55:
        cautions.append("short-term RSI spike may be noisy")

    if macd1h:
        if macd1h["bullish"]:
            score += 1; notes.append("MACD bullish")
        if macd1h["improving"]:
            score += 1; notes.append("MACD improving")
        if not macd1h["bullish"] and not macd1h["improving"]:
            cautions.append("MACD weak")

    if recent_6h is not None:
        if 1 < recent_6h < 12:
            score += 1; notes.append("recent follow-through")
        elif recent_6h < -2:
            cautions.append("recent hourly fade")
        elif recent_6h > 15:
            cautions.append("short-term move may be too stretched")

    if false_break["flag"]:
        score -= 2
        cautions.extend(false_break["reasons"])

    if intraday_range > 45 and qv < 20_000_000:
        cautions.append("wide range with suspect quality")
    if trades < 3000 and qv < 10_000_000:
        cautions.append("low trade count")

    news = run_news_check(symbol) if with_news else None
    if news:
        verdict = news.get("summary", {}).get("verdict")
        if verdict == "supportive":
            score += 1; notes.append("news support found")
        elif verdict == "risk":
            score -= 1; cautions.append("negative news risk")
        elif verdict == "hypey":
            cautions.append("headline hype risk")

    rating = "watch"
    if score >= 10 and "thin volume" not in cautions and "1h RSI extreme" not in cautions and not false_break["flag"]:
        rating = "candidate"
    elif score < 7:
        rating = "pass"

    return {
        "symbol": symbol,
        "price": last,
        "change_24h_pct": round(change, 3),
        "quote_volume": qv,
        "distance_to_high_pct": round(distance_high, 2),
        "intraday_range_pct": round(intraday_range, 2),
        "trade_count": trades,
        "rsi_15m": None if rsi15 is None else round(rsi15, 2),
        "rsi_1h": None if rsi1h is None else round(rsi1h, 2),
        "rsi_4h": None if rsi4h is None else round(rsi4h, 2),
        "macd_1h": macd1h,
        "recent_6h_return_pct": None if recent_6h is None else round(recent_6h, 2),
        "false_breakout": false_break,
        "news": news,
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
    ap.add_argument("--with-news", action="store_true")
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
        scored = score_symbol(t, with_news=args.with_news)
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
        print(f"   24h={r['change_24h_pct']:.2f}% | vol=${r['quote_volume']:,.0f} | dist_high={r['distance_to_high_pct']:.2f}%")
        print(f"   RSI 15m/1h/4h = {r['rsi_15m']} / {r['rsi_1h']} / {r['rsi_4h']}")
        if r['macd_1h']:
            m = r['macd_1h']
            print(f"   MACD1h bullish={m['bullish']} improving={m['improving']} hist={m['hist']}")
        print(f"   why: {', '.join(r['notes']) if r['notes'] else 'n/a'}")
        if r['cautions']:
            print(f"   caution: {', '.join(r['cautions'])}")
        if r['news']:
            s = r['news'].get('summary', {})
            print(f"   news: verdict={s.get('verdict')} pos={s.get('positive_hits')} neg={s.get('negative_hits')} hype={s.get('hype_hits')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
