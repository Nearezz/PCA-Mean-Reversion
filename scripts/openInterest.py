import ccxt 

exchange = ccxt.hyperliquid()
markets = exchange.load_markets()
symbols = exchange.symbols


tickers = exchange.fetch_tickers()
sample_ticker = tickers['BTC/USDC:USDC']['info']

valid_tickers = [
    (symbol, data)
    for symbol, data in tickers.items()
    if data is not None and data.get('info',{}).get('openInterest') is not None
]

N = 20
sorted_tickers = sorted(valid_tickers,key=lambda x: x[1]['quoteVolume'],reverse=True)
top_coins = []

for symbol, data in sorted_tickers:
    base = symbol.split("/")[0]
    top_coins.append(base)
    if len(top_coins) == N:
        break

print(top_coins)