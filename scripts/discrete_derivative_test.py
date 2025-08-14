import pandas as pd
import numpy as np
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(ROOT_DIR, "results")
DATA_DIR = os.path.join(ROOT_DIR, "data")

time_frame = "4h"
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


        residual_vector = prices_centered @ principal_vector_two
        residual_mean = residual_vector.mean()
        residual_std = residual_vector.std(ddof=1)
        residual_min = residual_vector.min()
        residual_max = residual_vector.max()

        secent_slope = np.diff(residual_vector).mean() 


        return {
        "Asset Pair": f"{sym1.split('_')[0]}–{sym2.split('_')[0]}",
        # "Principal Component 1 Variance (%)": round(var_1 * 100,2),
        # "Principal Component 2 Variance (%)": var_2 * 100,
        "Residual Mean" : residual_mean,
        "Residual STD" : round(residual_std,3),
        "Residual Min/Max": f"{round(residual_min,3)}/{round(residual_max,3)}",
        "Average Slope": secent_slope,
        
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
    df_results["Average Slope"] = df_results["Average Slope"].abs()
    df_results = df_results.sort_values(by="Average Slope", ascending=True)
    df_results['Average Slope'] = df_results["Average Slope"].apply(lambda x: f"{x:.2E}")
    df_results['Residual Mean'] = df_results['Residual Mean'].apply(lambda x: f"{x:.2E}" )
    # df_results['Principal Component 2 Variance (%)'] = df_results["Principal Component 2 Variance (%)"].apply(lambda x: f"{x:.2E}")
    print(df_results.head())


    # output_csv = os.path.join(RESULT_DIR, f"{time_frame}_second_table_results.csv")    
    # df_results.to_csv(output_csv, index=False)
    # print(f"Results saved to {output_csv}")

    output_tex = os.path.join(RESULT_DIR, f"{time_frame}_second_table_results.tex")
    df_results.to_latex(output_tex, index=False, float_format="%.2E")
    print(f"LaTeX table saved to {output_tex}")