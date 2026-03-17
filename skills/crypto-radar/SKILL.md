---
name: crypto-radar
description: Scan Binance USDT markets for short-term momentum candidates and false-breakout risks. Use when the user asks for crypto radar, pump radar, gainers analysis, breakout candidates, multi-check validation, RSI/volume/news cross-checks, or periodic market scans for coins worth watching or buying.
---

# Crypto Radar

Use this skill to find Binance spot pairs worth watching with a conservative multi-check process.

## Core rule

Do not recommend a coin from price change alone. Always validate with:

1. 24h price change
2. 24h quote volume
3. distance to 24h high
4. RSI on 1h candles
5. simple momentum structure
6. obvious risk flags

## Primary workflow

Run:

```bash
python3 {baseDir}/scripts/radar_scan.py
```

Optional arguments:

```bash
python3 {baseDir}/scripts/radar_scan.py --limit 8 --min-volume 5000000 --min-change 6
python3 {baseDir}/scripts/radar_scan.py --json
```

## How to interpret

### Worth watching
A coin is worth watching when most of these are true:
- 24h quote volume is healthy
- 24h change is strong but not only a low-liquidity spike
- price is close to the 24h high
- 1h RSI is strong but not absurdly overheated
- score is supported by multiple checks

### Possible buy candidate
A coin can be framed as a possible buy candidate only when:
- it passes the watchlist checks
- there is no obvious liquidity red flag
- the user understands this is a speculative setup, not certainty
- the recommendation is phrased as a conditional setup, not a guarantee

### Avoid / no alert
Do not alert when:
- no symbol reaches the score threshold
- symbols are mostly stablecoins or low-liquidity spikes
- RSI is extreme and volume quality is weak
- results look noisy or unconvincing

## Response style

For each strong candidate, include:
- symbol
- 24h % change
- 24h volume
- distance from 24h high
- 1h RSI
- short reason
- caution

If no candidate looks good enough, reply exactly:

`NO_REPLY`

## Important limits

- This skill is for spot market scanning and idea generation, not guaranteed profit.
- Prefer conservative language like "worth watching", "possible setup", or "high risk momentum".
- Never present a scan result as certain profit.
- Ignore futures, leverage, withdrawals, and transfers unless the user explicitly asks.
