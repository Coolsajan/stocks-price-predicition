import pandas as pd
import yfinance as yf
import datetime


class GetData:
    def __init__(self):
        pass
        
    def get_data(self,company_ticker,start_date  ,end_date ) :
        """Fentching the date for the comapany from the api"""

  
        ticker=yf.Ticker(company_ticker)
        comp_dataset=ticker.history(start=start_date,end=end_date)

        company_name=ticker.info["longName"]

        
        return comp_dataset ,company_name

