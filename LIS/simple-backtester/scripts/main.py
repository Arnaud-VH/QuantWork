import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = yf.download("AAPL", start="2024-01-01", end="2025-01-01")

print(data.tail())

#Calculate moving averages
data["SMA20"] = data["Close"].rolling(window=20).mean()
data["SMA50"] = data["Close"].rolling(window=50).mean()

data["Signal"] = 0

#Go through the lines in the data
data.loc[data["SMA20"] > data["SMA50"], "Signal"] = 1 #Buy Signal
data.loc[data["SMA20"] < data["SMA50"], "Signal"] = -1 #Sell Signal

print(data[["Close", "SMA20", "SMA50", "Signal"]].tail())

initial_cash = 10_000
position = 0

cash = initial_cash
portfolio_values = []

for date, row in data.iterrows():
   price = row["Close"].iloc[0] if hasattr(row["Close"], 'iloc') else row["Close"]
   signal = row["Signal"].iloc[0] if hasattr(row["Signal"], 'iloc') else row["Signal"]

   if signal == 1 and cash > 0:
      position = (cash / price)
      cash = 0
   
   elif signal == -1 and position > 0:
      cash = position * price
      position = 0
   
   total_value = cash + (position * price)
   portfolio_values.append(total_value)

data["Portfolio Value"] = portfolio_values

#Calculate some performance metrics
data["Daily Return"] = data["Portfolio Value"].pct_change()

total_return = (data["Portfolio Value"].iloc[-1] - initial_cash) / initial_cash * 100

#Annualized volatility assumes 252 trading days
volatility = data["Daily Return"].std() * np.sqrt(252)

sharpe_ratio = data["Daily Return"].mean() / data["Daily Return"].std() * np.sqrt(252)

print(f"Total Return: {total_return:.2f}%")
print(f"Annualized Volatility: {volatility:.2f}")
print(f"Shapre Ratio: {sharpe_ratio:.2f}")

#Plot the figure
plt.figure(figsize=(12,6))

plt.plot(data.index, data["Close"], label="AAPL Price", alpha=0.5)

plt.plot(data.index, data["SMA20"], label="20-Day SMA", alpha=0.75)

plt.plot(data.index, data["SMA50"], label="50-Day SMA", alpha=0.75)

plt.scatter(data.index[data["Signal"] == 1], data["Close"][data["Signal"] == 1],
             label="Buy Signal", marker="^", color="green", alpha = 1)

plt.scatter(data.index[data["Signal"] == -1], data["Close"][data["Signal"] == -1],
             label="Sell Signal", marker="v", color="red", alpha = 1)

plt.title("Moving Average Crossover Strategy")

plt.legend()

plt.savefig("moving_average_strategy.png", dpi=300, bbox_inches="tight")

#Now the portfolio value over time
plt.figure(figsize=(12,6))

plt.plot(data.index, data["Portfolio Value"], label="Portfolio Value", color="blue")

plt.title("Portfolio Performance Over Time")

plt.xlabel("Date")

plt.ylabel("Portfolio Value ($)")

plt.legend()

plt.savefig("portfolio_value_sma_strategy", dpi=300, bbox_inches="tight")

#Save results into CSV file
data.to_csv("../data/backtest_results.csv")
print("Backtest results saved to data/backtest_results.csv")