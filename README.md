**PCA-Mean-Reversion**

This repository implements a quantitative trading strategy based on Principal Component Analysis (PCA) and mean reversion. By reducing correlated assets (e.g., stock pairs) into principal components, this approach helps identify statistically stationary spreads suitable for pair trading or statistical arbitrage.


**Strategy Overview**

The core idea is:

Use PCA to decompose price data from two or more correlated assets.

Identify the first principal component (PC1) as the market direction.

Construct a residual (mean-reverting) spread orthogonal to PC1.

Use the Augmented Dickey-Fuller (ADF) test to verify stationarity.

Generate long/short signals based on z-score thresholds of the spread.

