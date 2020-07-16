Ticker = "BTCUSD"

class MovingAverageCrossAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        
        self.SetStartDate(2017, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(10000)
        self.AddCrypto(Ticker, Resolution.Daily, Market.GDAX)
        self.SetBrokerageModel(BrokerageName.GDAX, AccountType.Cash)
        self.SetBenchmark(Ticker)

        # create two Moving Averages
        self.fast = self.EMA(Ticker, 50, Resolution.Daily)
        self.slow = self.EMA(Ticker, 150, Resolution.Daily)
        self.middle = self.EMA(Ticker, 75, Resolution.Daily)

        self.previous = None
        self.Flag = "OK"
        self.Days = 0
        self.SellDay = -999




    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        
        
        # wait for our slow ema to fully initialize
        if not self.slow.IsReady:
            return
        
        # only once per day
        if self.previous is not None and self.previous.date() == self.Time.date():
            return
        
        ## start counter of how many days we have been live
        self.Days = self.Days + 1 
        
        self.Log("Day live:{}".format(self.Days))
        self.Log("SellDay:{}".format(self.SellDay))
        DaysSinceSell = self.Days-self.SellDay
        self.Log("Days since Sell:{}".format(DaysSinceSell))

        ## reset flag status if possible
        if self.fast.Current.Value<self.slow.Current.Value or DaysSinceSell>21:
            self.Flag = "OK"
            self.Log("Ready to Trade Again.")
            
        if self.Flag == "WAIT":
            self.Log("Waiting...")
            return


        # define a small tolerance on our checks to avoid bouncing
        tolerance = 0.05

        holdings = self.Portfolio[Ticker].Quantity

        ### CHARTING / VISUALIZING
        
        self.Plot("Data Chart","Fast EMA", self.fast.Current)
        self.Plot("Data Chart","Slow EMA", self.slow.Current)
        self.Plot("Data Chart","Middle EMA", self.middle.Current)
        self.Plot("Data Chart","Asset Price", self.Securities[Ticker].Price)


        # we only want to go long if we're currently short or flat
        if holdings <= 0:
            # if the fast is greater than the slow, we'll go long
            if self.fast.Current.Value > self.slow.Current.Value *(1 + tolerance):
                self.Log("BUY  >> {0}".format(self.Securities[Ticker].Price))
                self.Log("FAST EMA >> {}".format(self.fast.Current.Value))
                self.Log("SLOW EMA >> {}".format(self.slow.Current.Value))
                self.SetHoldings(Ticker, 1.0)

        # we only want to liquidate if we're currently long
        # if the fast is less than the slow we'll liquidate our long
        if holdings > 0 and self.fast.Current.Value < self.middle.Current.Value:
            self.Log("SELL >> {0}".format(self.Securities[Ticker].Price))
            self.Log("FAST EMA >> {}".format(self.fast.Current.Value))
            self.Log("MID EMA >> {}".format(self.middle.Current.Value))
            self.Log("SLOW EMA >> {}".format(self.slow.Current.Value))
            self.Liquidate(Ticker)
            self.Flag = "WAIT"
            self.SellDay = self.Days



        self.previous = self.Time