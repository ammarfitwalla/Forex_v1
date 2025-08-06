import yfinance as yf

# Define the ticker symbol
ticker_symbol = "EURUSD=X"  # Example: EUR/USD Forex pair

# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

# Fetch the ticker information
historical_data = yf.download(ticker_symbol, period="1mo", interval="5m")


# # Fetch historical market data for the last 30 days
# historical_data = ticker.history(period="5m")  # data for the last month

# Display a summary of the fetched data
print(f"Summary of Historical Data for {ticker_symbol}:")
print(historical_data[['Open', 'High', 'Low', 'Close', 'Volume']])