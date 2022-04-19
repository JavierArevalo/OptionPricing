from yahoo_fin import options
from yahoo_fin import stock_info as si


class Option:
    def _init_(self, ticker):

        Option = options.get_options_chain("nflx")
        dates = options.get_expiration_dates(ticker)

        self.ticker = ticker

        self.S = si.get_live_price(ticker)
        self.K = Option.loc[0,"Strike"]
        self.R = Option.loc[0,"Open Interest"]
        self.V = Option.loc[0,"Implied Volatility"]
        self.B = Option.loc[0,"Bid"]
        self.A = Option.loc[0,"Ask"]
        self.T = dates(0)
    
    def getOptionsData(self, ticker=None):
        if (ticker is None):
            ticker = self.ticker 
        
        optionData = options.get_options_chain(ticker)

        return optionData





