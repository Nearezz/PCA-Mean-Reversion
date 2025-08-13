import pandas as pd
import numpy as np
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(ROOT_DIR, "results")
DATA_DIR = os.path.join(ROOT_DIR, "data")

time_frame = "1m"
data_csv = os.path.join(DATA_DIR,f"close_prices/{time_frame}_close_for_all_tickers.csv")
df = pd.read_csv(data_csv)
cols = [c for c in df.columns if c != "timestamp"]
combs = list(combinations(cols,2))

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
        total_var = sum(singular_vals_squared)
        var_1 = singular_vals_squared[0]/total_var
        var_2 = singular_vals_squared[1]/total_var


        projecting_onto_pc2 = prices_centered @ principal_vector_two
        secent_slope = np.diff(projecting_onto_pc2).mean() 

        return {
        "Asset Pair": f"{sym1.split('_')[0]}–{sym2.split('_')[0]}",
       "Discrete Derivative": secent_slope,
        "Principal Component 1 Variance (%)": var_1 * 100,
        "Principal Component 2 Variance (%)": var_2 * 100
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
        for future in as_completed(futures_pairs):
            res = future.result()
            if res:
                results.append(res)

    df_results = pd.DataFrame(results)
    df_results["Discrete Derivative"] = df_results["Discrete Derivative"].abs()
    df_results = df_results.sort_values(by="Discrete Derivative", ascending=True)
    output_csv = os.path.join(RESULT_DIR, f"{time_frame}_discrete_derivative_results.csv")    
    df_results.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")
