import yfinance as yf
# import numpy as np
import pandas as pd
# from datetime import datetime, timedelta

# Function to calculate RSI (Relative Strength Index)
def get_rsi(file, value, n):
    """
    Calculates RSI (Relative Strength Index) for the given column.
    Takes arguments:
        - file (DataFrame): DataFrame containing the data
        - value (str): column name to calculate RSI on
        - n (int): period for the RSI calculation
    Returns:
        - DataFrame with a new column for RSI values
    """
    delta = file[value].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(span=n, adjust=False).mean()
    ema_down = down.ewm(span=n, adjust=False).mean()
    rs = ema_up / ema_down
    file[value + '_rsi'] = 100 - (100 / (1 + rs))
    print(f"RSI for {value} calculated with period {n}")
    return file


# Function to calculate moving averages (slow and fast)
def moving_avg(ultratech_df, value, slow_p, fast_p, slow_ma_col_name, fast_ma_col_name):
    """
    Calculates slow and fast moving averages for the given column.
    Takes arguments:
        - ultratech_df (DataFrame): DataFrame containing the data
        - value (str): column name to calculate moving averages on
        - slow_p (int): period for the slow moving average
        - fast_p (int): period for the fast moving average
        Returns:
        - DataFrame with columns for slow and fast moving averages
    """
    ultratech_df[slow_ma_col_name] = ultratech_df[value].rolling(window=slow_p, min_periods=1).mean()
    ultratech_df[f'{slow_ma_col_name}_period'] = slow_p
    ultratech_df[fast_ma_col_name] = ultratech_df[value].rolling(window=fast_p, min_periods=1).mean()
    ultratech_df[f'{fast_ma_col_name}_period'] = fast_p
    print(f"Moving averages for {value} calculated with slow period {slow_p} and fast period {fast_p}")
    return ultratech_df


# Function to fetch data from Yahoo Finance and process it
def get_data_yf(currency_name, interval):
    """Fetches Forex data (EUR/USD) from Yahoo Finance and processes it with RSI and moving averages."""
    try:
        # Fetch historical data from Yahoo Finance
        data = yf.download(currency_name, period="1mo", interval=interval)
        
        data.columns = data.columns.droplevel(1)  # Remove the 'Ticker' part of the MultiIndex
        # print("Columns after renaming:")
        # print(data.tail())  # Display the first few rows of the data
        # print(data.columns)
        # Calculate RSI for high and low columns
        data = get_rsi(data, 'High', 14)
        data = get_rsi(data, 'Low', 14)

        data = moving_avg(data, value='High', slow_p=17, fast_p=7, slow_ma_col_name='high_sma', fast_ma_col_name='high_fma')
        data = moving_avg(data, value='Low', slow_p=17, fast_p=7, slow_ma_col_name='low_sma', fast_ma_col_name='low_fma')

        # Handle missing values
        data = data.fillna(data.mean())
        data.reset_index(inplace=True)  # Reset index to have 'Datetime' as a column
        data['Datetime'] = pd.to_datetime(data['Datetime'])  # Ensure 'Datetime' is in datetime format
        

        return data.tail(5000)  # Keep the latest 5000 rows

    except Exception as e:
        print(f"Error: {e}")
        return None