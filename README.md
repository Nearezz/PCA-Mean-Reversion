# 📈 PCA Pairs Trading (Exploratory Project)

## Overview  
This project explores how **Principal Component Analysis (PCA)** can be applied to pairs trading.  
The idea is to decompose the joint price movements of two correlated assets into orthogonal components, and then study whether one of the components (a residual spread) behaves in a **mean-reverting** way.  

This repository is a **work in progress** — the goal is not to present a final trading system, but to experiment with PCA-based methods, check assumptions like stationarity, and eventually build towards a systematic approach.

---

## Current Steps  

### 1. Data Preparation  
- Collect price series for two correlated assets.  
- Normalize / mean-center the data so PCA focuses on **co-movement** rather than absolute prices.  

### 2. PCA Decomposition  
- Apply PCA (via SVD) to the price matrix.  
- The **first component** usually captures the broad market direction.  
- The **second component (PC2)** often represents the “residual spread” — the part orthogonal to the main trend.  

### 3. Residual Analysis  
- Project the price data onto PC2 to extract the spread.  
- Use **discrete derivatives** (slopes between points) to check whether the spread drifts significantly over time.  
- If the average slope is small, the spread may be a candidate for mean-reversion.  

### 4. Spread Visualization  
- Plot the spread, rolling mean, and standard deviation.  
- Compute **z-scores** to see how often the spread deviates from its mean.  

---

## Next Steps / To-Do  
- ✅ Basic PCA decomposition  
- ✅ Residual slope (stationarity check)  
- ⬜ More rigorous statistical stationarity tests (ADF, KPSS, Hurst exponent)  
- ⬜ Refine rolling window methods  
- ⬜ Backtest simple long/short signals  
- ⬜ Extend to multi-asset PCA (basket trading)  

---

## Notes  
This is an **educational / exploratory project**.  
The main goal is to learn how PCA can uncover hidden relationships between assets, and to evaluate whether those relationships can be turned into consistent trading strategies.  
