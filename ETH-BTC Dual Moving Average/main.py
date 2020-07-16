class MovingAverageCrossAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        
        self.SetStartDate(2017, 1, 1)   
        self.SetEndDate(2020, 1, 1)     
        self.SetCash(10000)             
        self.AddCrypto("BTCUSD", Resolution.Daily, Market.GDAX)
        self.AddCrypto("ETHUSD", Resolution.Daily, Market.GDAX)
        
        # create Moving Averages & Relative Differences 
        self.fastBTC = self.EMA("BTCUSD", 50, Resolution.Daily)
        self.slowBTC = self.EMA("BTCUSD", 200, Resolution.Daily)
        
        self.fastETH = self.EMA("ETHUSD", 50, Resolution.Daily)
        self.slowETH = self.EMA("ETHUSD", 200, Resolution.Daily)

        self.previous = None
        
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        
        # wait for our slow ema to fully initialize
        if not self.slowBTC.IsReady or not self.slowETH.IsReady:
            return
        
        # only once per day
        if self.previous is not None and self.previous.date() == self.Time.date():
            return
        
        ### Intialise Vairables

        reldifETH = (self.fastETH.Current.Value - self.slowETH.Current.Value)/self.slowETH.Current.Value
        reldifBTC = (self.fastBTC.Current.Value - self.slowBTC.Current.Value)/self.slowBTC.Current.Value

        holdingsBTC = self.Portfolio["BTCUSD"].Quantity
        holdingsETH = self.Portfolio["ETHUSD"].Quantity
        
        ### CHARTING / VISUALIZING
        
        self.Plot("Data Chart-BTC","Fast EMA", self.fastBTC.Current)
        self.Plot("Data Chart-BTC","Slow EMA", self.slowBTC.Current)
        self.Plot("Data Chart-BTC","Asset Price", self.Securities["BTCUSD"].Price)
        
        self.Plot("Relative Difference","RelDifBTC", reldifBTC)
        self.Plot("Relative Difference","RelDifETH", reldifETH)
        
        self.Plot("Data Chart-ETH","Fast EMA", self.fastETH.Current)
        self.Plot("Data Chart-ETH","Slow EMA", self.slowETH.Current)
        self.Plot("Data Chart-ETH","Asset Price", self.Securities["ETHUSD"].Price)
        
        
        ##### LOGIC TRADING ############
        
        ## If no crypto has been bought

        if holdingsBTC + holdingsETH <= 0:

            if reldifETH > reldifBTC and reldifETH > 0:
                self.SetHoldings("ETHUSD", 1.0)

            if reldifBTC > reldifETH and reldifBTC > 0:
                self.SetHoldings("BTCUSD", 1.0)

            return
        
        if holdingsBTC > 0:
            
            if reldifBTC < 0:
                self.Liquidate("BTCUSD")
            
            if reldifETH > reldifBTC and reldifETH > 0.10:
                self.Liquidate("BTCUSD")
                self.SetHoldings("ETHUSD", 1.0)

        if holdingsETH > 0:

            if reldifETH < 0:
                self.Liquidate("ETHUSD")
            
            if reldifBTC > reldifETH and reldifBTC > 0.10:
                self.Liquidate("ETHUSD")
                self.SetHoldings("BTCUSD", 1.0)

        self.previous = self.Time