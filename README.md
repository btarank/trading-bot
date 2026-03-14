# Binance Futures Testnet — Trading Bot

A Python CLI application to place **Market**, **Limit**, and **Stop-Limit** orders on the **Binance Futures Testnet (USDT-M)**.

Built with clean layered architecture: validators → API client → order logic → CLI.

---



## Setup

### 1. Get Testnet API Keys

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with GitHub or Google
3. Click your profile → **API Management** → **Create API**
4. Copy your **API Key** and **Secret Key**
5. Click **"Get 10,000 USDT"** to fund your testnet wallet

### 2. Clone & Install

```bash
git clone https://github.com/yourusername/trading-bot.git
cd trading-bot
pip install -r requirements.txt
```

### 3. Configure `.env`

Create a `.env` file in the project root:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

---

## How to Run

### Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Limit Order

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 50000
```

### Stop-Limit Order *(bonus)*

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type STOP --quantity 0.001 --price 40000 --stop-price 41000
```

> `--price` = the limit price (execute at this price)  
> `--stop-price` = the trigger price (activates the order when hit)

### View All Options

```bash
python cli.py --help
```

---

## Logging

All API requests, responses, and errors are logged to `logs/trading_bot.log`.

Example log output:

```
2024-01-15 10:23:41 | INFO     | client | BinanceFuturesClient initialized | testnet=True
2024-01-15 10:23:41 | INFO     | client | API REQUEST  | futures_create_order | params={'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001}
2024-01-15 10:23:42 | INFO     | client | API RESPONSE | success | response={...}
2024-01-15 10:23:42 | INFO     | orders | Order complete | orderId=123456 status=FILLED executedQty=0.001
```

---

## Assumptions

- Only **USDT-M Futures Testnet** is supported (not Spot or Coin-M)
- Symbols must end with `USDT` (e.g. `BTCUSDT`, `ETHUSDT`, `BNBUSDT`)
- `STOP` order type implements a **Stop-Limit** order with both a trigger price and a limit price
- `timeInForce` is set to `GTC` (Good Till Cancelled) for LIMIT and STOP orders
- Logs are written relative to the directory where you run `python cli.py`

---

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies
