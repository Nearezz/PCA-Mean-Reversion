import pandas as pd
import numpy as np
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor, as_completed
from statsmodels.tsa.stattools import adfuller
import os
from tqdm import tqdm

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(ROOT_DIR, "results")

time_frame = "1m"
data_csv = os.path.join(RESULT_DIR,f"close_prices/{time_frame}_close_for_all_tickers.csv")
df = pd.read_csv(data_csv)
cols = [c for c in df.columns if c != "timestamp"]
combs = list(combinations(cols,2))




MAXLAG = 0
def process_pair(sym1,sym2):
    try: 
        close1 = df[sym1]
        close2 = df[sym2]

        min_len = min(len(close1),len(close2))
        close1 = close1[:min_len]
        close2 = close2[:min_len]


        prices = np.column_stack([close1,close2])
        prices_centered = prices - prices.mean(axis=0)

        U,S,Vt = np.linalg.svd(prices_centered,full_matrices=False)
        principal_vector_one = Vt[0]
        principal_vector_two = Vt[1]


        singular_vals_squared = [v**2 for v in S]
        n = prices.shape[0]
        lambda_1 = singular_vals_squared[0]/ (n-1)
        lambda_2 = singular_vals_squared[1]/(n-1)
        total_var = lambda_1 + lambda_2
        lambda_1_pct = (lambda_1 / total_var) * 100
        lambda_2_pct = (lambda_2 / total_var) * 100

        projecting_onto_pc2 = prices_centered @ principal_vector_two
        secent_slope = np.diff(projecting_onto_pc2).mean() 

        return {
        "Pair": f"{sym1.split('_')[0]}–{sym2.split('_')[0]}",
        "Discrete Derivative": secent_slope 
    }
    except Exception as e:
            print(f"Error with {sym1} and {sym2}: {e}")

if __name__ == "__main__":
    results = []
    max_worker = os.cpu_count()

    with ProcessPoolExecutor(max_workers=max_worker) as executor:
        futures_pairs = [
            executor.submit(process_pair, sym1, sym2)
            for sym1, sym2 in combs
        ]
        for future in tqdm(as_completed(futures_pairs)):
            res = future.result()
            if res:
                results.append(res)

    df_results = pd.DataFrame(results)
    df_results["Discrete Derivative"] = df_results["Discrete Derivative"].abs()
    df_results = df_results.sort_values(by="Discrete Derivative", ascending=True)
    output_csv = os.path.join(RESULT_DIR, f"{time_frame}_discreate_derivative_results.csv")    
    df_results.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")
