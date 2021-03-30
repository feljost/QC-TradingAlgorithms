# QuantConnect Trading Algorithms

In this repository, you will find Trading Algorithms that have been developed on the QuantConnect Platform. If you want to run these scripts you will have to use the QuantConnect IDE which is available within your browser for free. Depending on how you want to use the scripts, some adjustments might be necessary. If you have any questions feel free to contact me.

## Table of Contents:
1. Dual Moving Average Strategy
2. ETH - BTC Relative Difference Dual Moving Average
3. Crypto Bandwagon Strategy (WIP)

### 1) Dual Moving Average Strategy

The dual moving average strategy is a simple trading strategy where we calculate 2 Exponential Moving Averages with two different windows. The Short Exponential Moving Average uses a window of 50 days, and the Long Moving Average uses a window of 200 days. If the Short Moving Average crosses the Long Moving Average from below, it indicates we are on an upward swing and will place a buy order. If the Short Moving Average crosses the Long moving Average from above, it indicates that we are on a downward swing and will place a sell order if we are long. Shorting is not a part of this strategy.

The performance of the strategy can be seen below (2015-2021). For the BTC-USD pair, it outperforms the buy and hold strategy. This specifically because it sells before the major downswing in April 2018 to April 2019.

![alt text](https://raw.githubusercontent.com/feljost/QC-TradingAlgorithms/master/Screenshots/BTCUSD_Single_Crypto_Strategy_Perfomance.png)

The strategy works especially well for assets with big horizontal swings, and not much sideways movement. For example, backtesting it on Macy's Stock ($M) gives us great results, significantly outperforming the market. If the stock tends to go sideways, however, this strategy will make numerous mistakes and too many trades, resulting in a lot of trading fees.

To improve this strategy the next step would be to identify what kind of assets have these horizontal swings and let the algorithm dynamically choose the right assets.

### 2) ETH - BTC Relative Difference Dual Moving Average 

The second strategy tracks 2 assets at once. For both assets (in this case ETH and BTC), the dual moving average strategy (described above) is applied, however, we also calculate how much the dual moving averages are apart from each other. If the two moving averages (for each respective asset) are far apart from each other, it indicates that the upward or downward trend seems to be of large magnitude. The strategy invests the money in the asset with the biggest positive difference between Short MA and Long MA. Intuitively, the script invests in the Asset which is going up the most.

This strategy will work great for Assets that are negatively correlated to each other. Like the normal Dual Moving Average Strategy (1), it will fail if there is too much sideways movement in the Asset Prices. 

The performance of the strategy can be seen below (2017-2021). It does not perform as well as the first strategy. This is mainly due to the strategy jumping around when to invest in BTC and when ETH and doing wrong and inefficient trades, and ETH and BTC being positively correlated.

![alt text](https://raw.githubusercontent.com/feljost/QC-TradingAlgorithms/master/Screenshots/ETH%2BBTC_Dual_Crypto_Strategy_Perfomance.png)

### 3) Crypto Bandwagon Strategy (WIP)

This strategy is inspired by the Crypto Bandwagon: http://thecryptobandwagon.com/. The Crypto Bandwagon Strategy invests into 3 cryptos each week, based on their previous 7-day performance compared to $USD. At the end of each week, 3 new cryptos are chosen (based on returns of last week) and the cycle is restarted.

Why does this work? Cryptocurrencies are often "Hype-Driven" and therefore people seem to be influenced by last week's returns. As such, it is possible to jump on the 'bandwagon' and (hopefully) jump off again before the price drops. This is based on the Autocorrelation of Cryptos (with 1-week lag) being positive, due to The Greater Fool Theory and Momentum Investing

For my initial testing, I took 11 popular cryptos on BitFinex as possible choices. Including all possibilities, unfortunately, breaks the strategy, as we get returns of +33m USD in one week, and then lose all in the next week. As such, the Strategy chooses the top 3 out of the 11 most popular Crypto-USD Pairings on BitFinex. It does outperform buying and holding bitcoin for the same time period.

The performance of the strategy can be seen below (2019.06-2019.12). 

![alt text](https://raw.githubusercontent.com/feljost/QC-TradingAlgorithms/master/Screenshots/BandWagon_Strategy_Perfomance.png)

While it does Perform extraordinarily well, there are some bugs in the code that still must be fixed and might improve performance. Namely, in some cases, the strategy isn't "quick enough" to use the QuantConnect command "SetHoldings" and therefore it tries to buy bigger quantities than the account has, as the price of the asset seems to fluctuate between getting the price data and issuing the buy order. 

A major drawback is the number of trades which are done each week. Each trade accumulates fees and therefore this strategy is quite fee heavy. Further experimentation and possible improvements could be made with stop-loss orders (like the original strategy) or trailing stop-loss orders.
