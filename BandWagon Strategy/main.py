n = 3 # Amount of Cryptos to invest in each week (with equal percentages)

# Define available cryptos to choose from
Tickers = ['BTCUSD','ETCUSD','LTCUSD','ETHUSD','ENJUSD',
           'EOSUSD','OMGUSD','NEOUSD','XLMUSD','XMRUSD','XRPUSD']

# Excluded as it gave an instant return of 33 Million (Extreme outlier): 

class BandWagonAlgo(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        
        self.SetStartDate(2020, 6, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(10000)
        for ticker in Tickers: #add all cryptos
            self.AddCrypto(ticker, Resolution.Daily, Market.Bitfinex)
        self.SetBrokerageModel(BrokerageName.Bitfinex, AccountType.Cash)
        self.SetBenchmark('BTCUSD')
        self.previous = None
        self.Days = 0
        self.Prices = []


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        
        # only once per day
        if self.previous is not None and self.previous.date() == self.Time.date():
            return
        
        prices = []
        for i, ticker in enumerate(Tickers): #get all prices and create list 
            price = self.Securities[ticker].Price
            prices.append(price)
        self.Prices.append(prices) 
        
        
        if self.Days % 7 == 0 and self.Days != 0: # Do this every 7 days
            
            #Calculate Weekly Perfomance
            returns = []
            for i, ticker in enumerate(Tickers):
                return_i = (self.Prices[self.Days][i] - self.Prices[self.Days-7][i]) / self.Prices[self.Days-7][i] #Calculate Weekly Perfomance
                returns.append(return_i)
            
            # Get top n performers
            top = sorted(range(len(returns)), key=lambda i: returns[i])[-n:]
            self.Log('Top Performers: {}'.format(top))
            
            
            # Sell assets which aren't in top performers
            for i, ticker in enumerate(Tickers):
                if self.Portfolio[ticker].Quantity != 0 and i not in top:
                    self.Liquidate(ticker)
                    self.Log('Sold {}'.format(ticker))
            
            # Temp: Buy new top performers which we dont have already
            for i in top:
                ticker_ = Tickers[i]
                if self.Portfolio[ticker_].Quantity == 0:
                    self.SetHoldings(ticker_, (1/n)*0.8) # keep a 20% cash buffer
                    self.Log('Bought {}'.format(ticker_))
            
        self.Days = self.Days + 1 #Count the days since going live