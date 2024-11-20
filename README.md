# Stock Trading Bot with Moving Averages

This project implements a **stock trading bot** that uses a moving average crossover strategy to generate buy/sell signals and evaluate its performance. The bot fetches historical stock data from the **Alpha Vantage API**, processes it, and visualizes the results.

---

## Features

### Data Fetching:
- Retrieves daily historical stock data using the [Alpha Vantage API](https://www.alphavantage.co/documentation/).
- Supports fetching full datasets for up to 20 years of historical data.

### Data Processing:
- Cleans and prepares the stock data for analysis.
- Calculates **10-day** and **50-day moving averages**.

### Signal Generation:
- Uses a moving average crossover strategy:
  - **BUY signal**: When the short-term moving average crosses above the long-term moving average.
  - **SELL signal**: When the short-term moving average crosses below the long-term moving average.

### Visualization:
- Plots stock prices, moving averages, and buy/sell signals on a graph for easy analysis.

### Performance Evaluation:
- Calculates:
  - Total Profit
  - Trading Volume
  - Average Return Per Trade

---

## Installation and Setup

### Prerequisites
- Python 3.x
- Required libraries: `requests`, `pandas`, `numpy`, `matplotlib`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ieatmomo/stock-trading-bot.git
   cd stock-trading-bot


2. Get an API key from Alpha Vantage and replace your_api_key in the code:
	```Python
	url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&outputsize=full&apikey=your_api_key"


### Usage:
**Running the Bot:**
 - Set the stock symbol (e.g., AAPL for Apple or TSLA for Tesla) in the Stock class initialization.

**Run the script:**
python stock_trading_bot.py

**The bot will:**

1. Fetch and prepare stock data.
2. Calculate moving averages and generate buy/sell signals.
3. Plot the stock prices and signals.
4. Print the evaluation metrics.

### Example Output:
**Visualization**
The bot generates a chart showing:

- Close Price: Stock price over time (solid line).
- Short-Term Moving Average (10 Days): Dashed line.
- Long-Term Moving Average (50 Days): Dash-dot line.
- Buy Signal: Green upward triangles.
- Sell Signal: Red downward triangles.

### Evaluation Metrics
**Example output:**

Total Profit: -1478.41
Trading Volume: 2221778994
Average Return Per Trade: -6.654172192610081e-07
### Code Structure
## Stock Class
# Methods:
- fetch_data(): Fetches stock data using Alpha Vantage API.
- prepare_data(): Cleans and preprocesses the data.
- calculating_moving_averages(): Calculates 10-day and 50-day moving averages.
- generate_signals(): Generates buy/sell signals based on moving average crossovers.
- plot_data(): Visualizes the stock prices, moving averages, and signals.
- total_profit(): Calculates the total profit from the strategy.
- trading_volume(): Calculates the total trading volume from executed trades.
- average_return_per_trade(): Computes the average return per trade.
- evaluate_performance(): Summarizes the strategy’s performance.

### Future Improvements
1. Optimize moving average parameters for better performance.
2. Introduce filters (e.g., RSI or Bollinger Bands) to reduce false signals.
3. Add support for transaction cost simulation.
4. Save results and visualizations to files for reporting.

### License
This project is licensed under the MIT License.

