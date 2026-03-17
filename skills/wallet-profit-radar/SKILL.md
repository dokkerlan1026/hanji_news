---
name: wallet-profit-radar
description: Review the user's Binance spot wallet and flag holdings worth trimming, taking profit on, or watching for downside risk. Use when checking wallet positions, profit protection, sell candidates, stop-loss review, or periodic portfolio scan automation.
---

# Wallet Profit Radar

Review Binance spot balances conservatively.

## Goal

Find positions that may deserve:
- take-profit consideration
- reduced exposure after a sharp pump
- caution if momentum fades
- no action if size is too small or setup is weak

## Run

```bash
python3 {baseDir}/scripts/check_wallet_positions.py
python3 {baseDir}/scripts/check_wallet_positions.py --min-usdt 5
python3 {baseDir}/scripts/check_wallet_positions.py --json
```

## Decision style

- Suggest, do not force.
- Ignore dust positions by default.
- Prefer phrases like "consider trimming", "watch closely", or "no action".
- If nothing meaningful is found, reply exactly `NO_REPLY`.
