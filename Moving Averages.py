import requests
import pandas as pd
import numpy as np
from json import JSONDecodeError
import matplotlib.pyplot as plt


class Stock:
    def __init__(self, symbol, data):
        self.symbol = symbol
        self.data = data

    def fetch_data(self):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&outputsize=full&apikey=your_api_key"
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

    def calculating_moving_averages(self):
        #10 day moving average
        df = self.df
        MA_10 = df["4. close"].rolling(10).mean()

        #50 day moving average
        MA_50 = df["4. close"].rolling(50).mean()

        df["6. MA_Short"] = MA_10
        df["7. MA_Long"] = MA_50

    def generate_signals(self):
        df = self.df
        df["8. Differences"] = df["6. MA_Short"] - df["7. MA_Long"]
        df["9. Sign Changes"] = np.sign(df["8. Differences"])
        df["10. Signals"] = df["9. Sign Changes"].diff()
        df["11. BUY or SELL"] = np.where(df["10. Signals"] == 2.0, "BUY", np.where(df["10. Signals"] == -2.0, "SELL", ""))

    def plot_data(self):
        df = self.df
        df.dropna(subset=["6. MA_Short", "7. MA_Long"], inplace=True)
        xpoints = df.index
        ypoints_close = np.array(df["4. close"])
        ypoints_short = np.array(df["6. MA_Short"])
        ypoints_long = np.array(df["7. MA_Long"])
        
        plt.plot(xpoints, ypoints_close, linestyle= 'solid', label="Close Price")
        plt.plot(xpoints, ypoints_short, linestyle='dashed', label="Short Term Moving Average (10 Days)")
        plt.plot(xpoints, ypoints_long, linestyle='dashdot', label="Long Term Moving Average (50 Days)")

        buy_signals_x = df.index[df["11. BUY or SELL"] == "BUY"]
        buy_signals_y = df["4. close"][df["11. BUY or SELL"] == "BUY"]

        sell_signals_x = df.index[df["11. BUY or SELL"] == "SELL"]
        sell_signals_y = df["4. close"][df["11. BUY or SELL"] == "SELL"]

        buy_signals_x_points = np.array(buy_signals_x)
        buy_signals_y_points = np.array(buy_signals_y)
        sell_signals_x_points = np.array(sell_signals_x)
        sell_signals_y_points = np.array(sell_signals_y)

        plt.scatter(buy_signals_x_points, buy_signals_y_points,color="green", marker="^", label="Buy Signal")
        plt.scatter(sell_signals_x_points, sell_signals_y_points, color ="red", marker="v", label="Sell Signal")
        plt.legend()
        plt.title("Stock Prices Over the Last 20 Years with Moving Averages and Trading Signals")
        plt.xlabel("Date")
        plt.ylabel("Stock Price (USD)")
        plt.show()

    def total_profit(self):
        df = self.df
        total_profit = 0
        last_buy_price = None

        for index, row in df.iterrows():
            signal = row["11. BUY or SELL"]

            if signal == "BUY" and last_buy_price is None:
                last_buy_price = row["4. close"]

            elif signal == "SELL" and last_buy_price is not None:
                sell_price = row["4. close"]
                profit = sell_price - last_buy_price
                total_profit += profit
                last_buy_price = None

        return total_profit

    def trading_volume(self):
        df = self.df
        total_trading_volume = 0

        for index, row in df.iterrows():
            if row["11. BUY or SELL"] in ["BUY", "SELL"]:
                total_trading_volume += row["5. volume"]

        return total_trading_volume

    def average_return_per_trade(self):
        profit = Stock.total_profit(self)
        trading_volume = Stock.trading_volume(self)

        average_return_per_trade = profit/trading_volume
        
        return average_return_per_trade

    def evaluate_performance(self):
        profit = Stock.total_profit(self)
        trades = Stock.trading_volume(self)
        avg = Stock.average_return_per_trade(self)
        print(f"Total Profit:{profit}")
        print(f"Trading Volume: {trades}")
        print(f"Average Return Per Trade: {avg}")
        return profit, trades, avg
        

if __name__ == "__main__":
    apple_stock = Stock("AAPL", None)
    apple_stock.fetch_data()
    apple_stock.prepare_data()
    apple_stock.calculating_moving_averages()
    apple_stock.generate_signals()
    apple_stock.plot_data()
    apple_stock.evaluate_performance()
    print(apple_stock.df.tail().to_string())