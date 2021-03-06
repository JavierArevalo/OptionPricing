from yahoo_fin import options
from yahoo_fin import stock_info as si
from datetime import datetime
from datetime import timedelta

class Options:
    def __init__(self, ticker,type):
        dates = options.get_expiration_dates(ticker)
        
        if type == "call":
            Option = options.get_calls("nflx",dates[0])

        if type == "put":
            Option = options.get_puts("nflx",dates[0])
 
        self.type = type
        self.ticker = ticker
        self.S = si.get_live_price(ticker) # Stock Price
        self.K = Option.loc[0,"Strike"] #Strike Price
        self.R = Option.loc[0,"Open Interest"] #Interest Rate
        self.V = Option.loc[0,"Implied Volatility"] #Implied Volatility
        self.B = Option.loc[0,"Bid"] #Bid Price
        self.A = Option.loc[0,"Ask"] #Ask Price

        dates = dates[0].split()
        month_number = datetime.strptime(dates[0], "%B").month
        day_number = dates[1].split(',')
        day_number = day_number[0]
        year_number = dates[2]

        self.T = datetime(int(year_number), month_number, int(day_number), 18, 0, 0)
    
    def getOptionsData(self, ticker=None):
        if (ticker is None):
            ticker = self.ticker 
        
        optionData = options.get_options_chain(ticker)

        return optionData

    def getTimeDiff(self):
        difference = self.T - datetime.now()
        time_diff = (difference.days + difference.seconds/86400)/365.2425

        return time_diff


def getStockPrice(ticker,date):

    startDate = date 
    startDate = startDate.strftime("%d/%m/%Y")
    endDate = date +  timedelta(days=1)
    endDate = endDate.strftime("%d/%m/%Y")
    few_days = si.get_data('AAPL' , start_date = startDate , end_date = endDate)
    val = float(few_days["adjclose"])

    return val

test = Options("nflx","call")
print(test.getTimeDiff())
time = datetime.strptime("18/04/2022", "%d/%m/%Y")
print(getStockPrice("AAPL",time))

