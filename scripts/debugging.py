import ccxt
import pandas as pd 
import time 
import os 


exchange = ccxt.binance()
symbol = 'ETH/USDT'
timeframe = '15m'
since = exchange.parse8601('2021-01-01T00:00:00Z')

# Fetch one batch with a far-back start time
try:
    candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=1000)
    if candles:
        print("Old candles returned. First candle:")
        print(pd.to_datetime(candles[0][0], unit='ms'))
    else:
        print("No data returned")
except Exception as e:
    print("Error:", e)