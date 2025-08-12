# PCA Pairs Trading Strategy

## Overview  
This repository implements a trading stratergy that uses **Principal Component Analysis (PCA)** to identify mean-reverting relationships between two correlated assets. By decomposing their price movements into orthogonal components, we isolate a residual spread that is uncorrelated with the primary market direction. This residual is checked for stability using **discrete derivatives**, ensuring it does not drift significantly over time. The spread is then monitored for deviations from its historical mean to generate systematic long/short trading signals.

## Strategy  

### 1. Data Preparation  
- Collect price series for two correlated assets.  
- Mean-center the data to remove average price levels.  

### 2. PCA Decomposition  
- Apply PCA (via Singular Value Decomposition) to the mean-centered price matrix.  
- Identify the **second principal component** (PC2) as the mean-reverting spread.  

### 3. Stationarity Check (Discrete Derivatives)  
- Project prices onto PC2 to obtain the residual spread.  
- Compute the slope between successive residual points.  
- Calculate the **average slope**; if it is below a small threshold (e.g., < 0.05), the spread is considered stable.  

### 4. Spread & Z-Score Calculation  
- Compute a rolling mean and standard deviation of the spread.  
- Calculate z-scores to measure deviation from the rolling mean.  

### 5. Signal Generation  
- **Entry:**  
  - Long the undervalued asset and short the overvalued asset when z-score exceeds the upper or lower 10% historical threshold.  
- **Exit:**  
  - Close positions when the spread reverts close to its mean (within a small ε-band).  

