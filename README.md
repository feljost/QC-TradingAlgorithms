# QC-TradingAlgorithms

QuantConnect Trading Algorithms created as a fun project. If you want to run these scripts you will have to use the QuantConnect IDE which is available within your browser for free. Depending on how you want to use the Script, some adjustments might be necessary.

Two Trading Strategies are in this Repository:

1. Dual Moving Average Strategy
2. ETH - BTC Relative Difference Dual Moving Average

### 1) Dual Moving Average Strategy

The dual moving average strategy is a simple trading strategy where we calculate 2 Exponential Moving Averages with two different windows. The Short Exponential Moving Average uses a window of 50 days, and the Long Moving Average uses a window of 200 days. If the Short Moving Average crosses the Long Moving Average from below, it indicates we are on an upward swing and will place a buy order. If the Short Moving Average crosses the Long moving Average from above, it indicates that we are on a downward swing and will place a sell order if we are long. Shorting is not a part of this strategy.

The perfomance of the strategy can be seen below (2015-2021). For BTC-USD Pair it outperforms the buy and hold strategy. This specifically because it sells bevore the major downsing in April 2018 to April 2019.

![alt text](https://raw.githubusercontent.com/feljost/QC-TradingAlgorithms/master/Screenshots/BTCUSD_Single_Crypto_Strategy_Perfomance.png)

The strategy works especially well for Assets with big up and down swings, and not much sideways movement. For example, back testing it on the Macy's Stock ($M) gives us great results, significantly outperforming the market. If the stock tends to go sideways however, this strategy will make numerous mistakes and too many trades, resulting in a lot of trading fees.

### 2) ETH - BTC Relative Difference Dual Moving Average 

The second strategy tracks 2 Assets at once. For both Assets (in this case ETH and BTC), the dual moving average strategy is applied, however, we also calculate how much the Dual Moving Averages are apart from each other. If the two moving averages (for each asset) are far apart from each other, it indicates that the upward or downward trend seems to be of large magnitude. The Strategy invests the money in the Asset with the biggest positive difference between Short MA and Long MA. Intuitively, the script invests in the Asset which is going up the most.

This strategy will work great for Assets which are (somewhat) negatively correlated to each other. Like the normal Dual Moving Average Strategy (1), it will fail if there is too much sideways movement in the Asset Prices. 

The perfomance of the strategy can be seen below (2017-2021). It does not perform as well as the first strategey. This is mainly due to the strategy jumping around when to invest in BTC and when ETH and doing wrong and inefficient trades.

![alt text](https://raw.githubusercontent.com/feljost/QC-TradingAlgorithms/master/Screenshots/ETH%2BBTC_Dual_Crypto_Strategy_Perfomance.png)
