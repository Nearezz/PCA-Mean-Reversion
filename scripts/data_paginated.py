import ccxt
import pandas as pd 
import time 
import os 


# Settings 
ALL_SYMBOLS = {
    'BTC': 'BTC/USDT',
    'ETH': 'ETH/USDT',
    'XRP': 'XRP/USDT',
    'SOL': 'SOL/USDT',
    'DOGE': 'DOGE/USDT',
    'AVAX': 'AVAX/USDT',
    'LTC': 'LTC/USDT'
}

SYMBOl = ALL_SYMBOLS['LTC']
TIMEFRAME = "3m"
START_DATE = '2021-01-01T00:00:00Z'  
OUTPUT_DIR = "../Data"

def fetch_ohlcv_paginated(exchange,symbol,timeframe,since_iso,output_folder):
   
    since = exchange.parse8601(since_iso)
    all_ohlcv = []
    limit = 1000

    while True:
        try:
            data = exchange.fetch_ohlcv(SYMBOl,timeframe=timeframe,since=since,limit=limit)
        except Exception as e:
            print("Error:",e)
            break
        if not data:
            break

        all_ohlcv.extend(data)
        since = data[-1][0] + 1
        time.sleep(exchange.rateLimit / 1000)

    df = pd.DataFrame(all_ohlcv,columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms').dt.strftime('%Y-%m-%d %H:%M')

    filename = f"{symbol.replace('/', '_')}_{timeframe}.csv"
    df.to_csv(os.path.join(OUTPUT_DIR, filename), index=False)


    print(f" Done. Saved {len(df)} rows to {filename}\n")
    return df



EXCHANGE = ccxt.binance()
MARKET = EXCHANGE.load_markets()
df = fetch_ohlcv_paginated(exchange=EXCHANGE,symbol=SYMBOl,timeframe=TIMEFRAME,since_iso=START_DATE,output_folder=OUTPUT_DIR)