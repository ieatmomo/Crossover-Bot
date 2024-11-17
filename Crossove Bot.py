#API KEY: 4J2ULQPDE9BFOJBB

import requests
import pandas as pd
from json import JSONDecodeError



class Stock:
    def __init__(self, symbol, data):
        self.symbol = symbol
        self.data = data

    def fetch_data(self):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&apikey=your_api_key"
        r = requests.get(url)

        if r.status_code != 200:
            print("Error")

        try:
            self.data = r.json()
        except JSONDecodeError:
            print("Error: Parsing Error")
            self.data = None

        if "Time Series (Daily)" not in self.data:
            self.data = None
            print("Error: Wrong Data")

    def prepare_data(self):
        self.data = self.data["Time Series (Daily)"]
        df = pd.DataFrame(self.data)
        df = df.transpose()
        df['1. open'] = pd.to_numeric(df['1. open'], errors="coerce")
        df['2. high'] = pd.to_numeric(df['2. high'], errors="coerce")
        df['3. low'] = pd.to_numeric(df['3. low'], errors="coerce")
        df['4. close'] = pd.to_numeric(df['4. close'], errors="coerce")
        df['5. volume'] = pd.to_numeric(df['5. volume'], errors="coerce")
        df.index = pd.to_datetime(df.index, errors="coerce")
        self.df = df
        print(self.df)

    def calculating_moving_averages(self):
        #10 day moving average
        df = self.df
        MA_10 = df["4. close"].rolling(10).mean()

        #50 day moving average
        MA_50 = df["4. close"].rolling(50).mean()

        print(MA_10, MA_50)
        
if __name__ == "__main__":
    apple_stock = Stock("AAPL", None)
    apple_stock.fetch_data()
    apple_stock.prepare_data()
    apple_stock.calculating_moving_averages()
    print(apple_stock)