# AI 幣圈日報 Workflow

## 目標

用已安裝的 skills 建立一個偏保守、研究優先的幣圈日常流程：

- `trading-research`
- `binance`
- `binance-trading-signal`

核心原則：

- 先研究，再交易
- 先現貨，再考慮更高風險工具
- API 權限只開 `Read` / `Trade`，不要開 `Withdraw`
- 單筆風險預設不超過總資金 1-2%

## 每日流程

### 1. 市場總覽

先看 BTC / ETH / SOL：

- 現價
- 24h 漲跌
- 成交量
- 1h / 4h 趨勢

建議命令：

```bash
cd skills/trading-research
python3 scripts/binance_market.py --symbol BTCUSDT --all
python3 scripts/binance_market.py --symbol ETHUSDT --all
python3 scripts/binance_market.py --symbol SOLUSDT --all
python3 scripts/technical_analysis.py --symbol BTCUSDT --interval 1h
python3 scripts/technical_analysis.py --symbol BTCUSDT --interval 4h
```

### 2. 市場機會掃描

找出：

- Top gainers
- 高成交量對
- 波動高的幣對
- breakout 候選

建議命令：

```bash
cd skills/trading-research
python3 scripts/market_scanner.py --gainers --limit 20
python3 scripts/market_scanner.py --volume
python3 scripts/market_scanner.py --volatile
python3 scripts/market_scanner.py --breakout
```

### 3. 聰明錢 / 鏈上訊號

重點看：

- Smart money buy/sell
- signal trigger price vs current price
- max gain
- exit rate
- Solana / BSC 新訊號

資料來源：`binance-trading-signal`

官方端點：

- `https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money`

預設觀察：

- `chainId: CT_501` = Solana
- `chainId: 56` = BSC

## 日報模板

### 市場概況
- BTC：
- ETH：
- SOL：
- 市場情緒：

### 今日強勢 / 異動標的
- Pair 1：
- Pair 2：
- Pair 3：

### Smart Money 訊號
- 新增買入訊號：
- 新增賣出訊號：
- 值得追蹤合約：

### 候選交易
每一筆都寫：
- 標的：
- 理由：
- 進場區：
- 止損：
- 止盈：
- 風險報酬比：
- 倉位建議：

### 今天不碰的東西
- 流動性太差
- 結構太亂
- 漲太急 / RSI 過熱
- smart money 已高 exit rate

## 下單前檢查表

### 現貨
- [ ] 有明確 thesis
- [ ] 有止損
- [ ] R:R >= 1.5
- [ ] 單筆風險 <= 2%
- [ ] 不是情緒單

### API / 安全
- [ ] 只開 Read / Trade
- [ ] 沒開 Withdraw
- [ ] 先 testnet / 小額
- [ ] 不把 API key 寫進 repo

## 對 3 個已裝 skill 的定位

### `trading-research`
- 研究主力
- 可直接跑腳本
- 偏保守、實用

### `binance`
- 偏操作手冊 / API 流程
- 適合之後接 Binance Spot API
- 強調 testnet-first

### `binance-trading-signal`
- 偏鏈上 Smart Money 訊號
- 適合拿來當早期雷達，不適合單獨當買入理由

## 建議使用順序

1. 先用 `trading-research` 做市場判讀
2. 再用 `binance-trading-signal` 補鏈上訊號
3. 最後才考慮用 `binance` 接 API 做查詢 / 測試單

## 不建議現在做的事

- 直接開 futures
- 直接自動下單
- 只憑一個 smart money signal 就追單
- 安裝可疑 skill 後直接給金鑰
