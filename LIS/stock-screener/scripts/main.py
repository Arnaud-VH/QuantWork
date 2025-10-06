import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

stock_list = ["AAPL", "MSFT", "ASML", "TSLA", "GOOGL"]

def get_stock_data(ticker):
   stock = yf.Ticker(ticker)

   info = stock.info
   return {
      "Ticker": ticker, 
      "Price": info.get("currentPrice"),
      "PE Ratio": info.get("trailingPE"),
      "Dividend Yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
      "Market Cap": info.get("marketCap")
   }

def build_screener(stock_list):
   ticker_list = stock_list
   data = []

   for ticker in ticker_list:
      try:
         stock_data = get_stock_data(ticker)

         data.append(stock_data)

      except Exception as e:
         print(f"Error retrieving data for {ticker}: {e}")
   
   return pd.DataFrame(data)

def filter_stocks(df):
   filtered = df[
      (df["PE Ratio"] < 30) & 
      (df["Dividend Yield"] > 0.5) & 
      (df["Market Cap"] > 50_000_000_000)
   ]

   return filtered

df = build_screener(stock_list)
filtered_df = filter_stocks(df)

print("Filtered Stocks:\n", filtered_df)

# filtered_df.to_excel("../data/filtered_stocks.xlsx", index=False)
# print("Filtered stocks saved to data/filtered_stocks.xlsx")

def plot_stock(ticker):
   stock = yf.Ticker(ticker)

   hist = stock.history(period="3y")

   plt.figure(figsize=(10, 5))

   plt.plot(hist.index, hist["Close"], label=f"{ticker} Price")

   plt.title(f"{ticker} - 3 Year Price History")

   plt.xlabel("Date")

   plt.ylabel("Price (USD)")

   plt.legend()
   
   plt.savefig("stock_plot.png", dpi=300, bbox_inches="tight")

if not filtered_df.empty:
   top_ticker = filtered_df.iloc[0]["Ticker"]
   plot_stock(top_ticker)