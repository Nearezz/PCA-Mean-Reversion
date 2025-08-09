import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(ROOT_DIR,"Data")
RESULTS_DIR = os.path.join(ROOT_DIR,"results")


timeframe = "1m"

data_csvs = {
    "AVAX" : os.path.join(DATA_DIR,f"{timeframe}_Data",f"AVAX_USDT_{timeframe}.csv"),
    "BTC" : os.path.join(DATA_DIR,f"{timeframe}_Data",f"BTC_USDT_{timeframe}.csv"),
    "DOGE" : os.path.join(DATA_DIR,f"{timeframe}_Data",f"DOGE_USDT_{timeframe}.csv"),
    "ETH" : os.path.join(DATA_DIR,f"{timeframe}_Data",f"ETH_USDT_{timeframe}.csv"),
    "LTC" : os.path.join(DATA_DIR,f"{timeframe}_Data",f"LTC_USDT_{timeframe}.csv"),
    "SOL" : os.path.join(DATA_DIR,f"{timeframe}_Data",f"SOL_USDT_{timeframe}.csv"),
    "XRP" : os.path.join(DATA_DIR,f"{timeframe}_Data",f"XRP_USDT_{timeframe}.csv")
}

def csv_loading(ticker,file_path):
   # created a new df
   df = pd.read_csv(
      file_path,
      usecols=["timestamp","close"],
      parse_dates=["timestamp"]
   )
   df.set_index("timestamp",inplace=True)
   df.rename(columns={"close": ticker},inplace=True)
   return df

max_workers = min(len(data_csvs),os.cpu_count() * 2)
dfs = []

with ThreadPoolExecutor(max_workers=max_workers) as executor: 
   futures = [executor.submit(csv_loading,ticker,file_path) for ticker,file_path in data_csvs.items()]
   for future in tqdm(as_completed(futures)):
      dfs.append(future.result())

close_df = pd.concat(dfs,axis=1,join="inner").sort_index()
print(close_df['BTC'].mean())
close_df.to_csv(f"{RESULTS_DIR}/{timeframe}_close_for_all_tickers.csv",index=True).sort

