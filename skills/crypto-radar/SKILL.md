---
name: crypto-radar
description: Scan Binance USDT markets for short-term momentum candidates with multi-check validation. Use when the user asks for crypto radar, pump radar, gainers analysis, breakout candidates, false-breakout checks, multi-timeframe RSI, MACD confirmation, or news cross-checks for coins worth watching or buying.
---

# 📡 Crypto Radar v2

Use this skill to find Binance spot pairs worth watching with a conservative multi-check process.

## 🧠 Core rule

Do not recommend a coin from price change alone.
Always validate with:

1. 📈 24h price change
2. 💵 24h quote volume
3. 🎯 Distance to 24h high
4. 📊 Multi-timeframe RSI (`15m`, `1h`, `4h`)
5. 🔄 `1h` MACD condition
6. 🪤 False-breakout checks
7. 📰 Simple news verification
8. 🚩 Obvious risk flags

## ⚙️ Primary workflow

Run:

```bash
python3 {baseDir}/scripts/radar_scan.py --with-news
```

Optional arguments:

```bash
python3 {baseDir}/scripts/radar_scan.py --with-news --limit 8 --min-volume 5000000 --min-change 6
python3 {baseDir}/scripts/radar_scan.py --with-news --json
python3 {baseDir}/scripts/news_check.py ZECUSDT
```

## ✅ Multi-check logic

### 👀 Worth watching
A coin is worth watching when most of these are true:
- 💧 24h quote volume is healthy
- 🚀 24h change is strong but not just a low-liquidity spike
- 🎯 Price is close to the 24h high
- 📊 RSI is aligned across multiple timeframes
- 🔄 MACD is bullish or improving
- 🪤 False-breakout signs are limited
- 📰 News is neutral-to-supportive, not obviously dangerous

### 🟢 Possible buy candidate
Frame a coin as a possible buy candidate only when:
- ✅ It passes the watchlist checks
- 🚫 There is no obvious liquidity red flag
- 🪤 False-breakout checks do not look bad
- 🧩 There is at least some technical or news support
- 🗣️ The recommendation is phrased as a conditional setup, not a guarantee

### 🔕 Avoid / no alert
Do not alert when:
- ❌ No symbol reaches the score threshold
- 🧊 Symbols are mostly stablecoins or low-liquidity spikes
- 🥵 RSI is extreme and volume quality is weak
- 📉 Latest structure looks like a failed breakout
- 📰 News looks mostly hype-driven or risky
- 🌫️ Results look noisy or unconvincing

## 📝 Response style

For each strong candidate, include:
- 🪙 Symbol
- 📈 24h % change
- 💵 24h volume
- 🎯 Distance from 24h high
- 📊 RSI `15m / 1h / 4h`
- 🔄 MACD read
- 📰 News verdict
- 💡 Short reason
- ⚠️ Caution

If no candidate looks good enough, reply exactly:

`NO_REPLY`

## 🛡️ Important limits

- 📍 This skill is for spot market scanning and idea generation, not guaranteed profit.
- 🗣️ Prefer conservative language like "worth watching", "possible setup", or "high risk momentum".
- 🚫 Never present a scan result as certain profit.
- 📰 News validation is only an extra check, not proof.
- ⛔ Ignore futures, leverage, withdrawals, and transfers unless the user explicitly asks.
