import os
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd
import pytz


def get_data_mt5(currency_name):
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    pd.set_option('display.max_columns', 500)  # number of columns to be displayed
    pd.set_option('display.width', 1500)  # max table width to display

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    utc_from = datetime.now(tz=pytz.utc) - timedelta(days=20)
    utc_to = datetime.now(tz=pytz.utc)

    ticks = mt5.copy_ticks_range(currency_name, utc_from, utc_to, mt5.COPY_TICKS_ALL)
    ticks_frame = pd.DataFrame(ticks)
    return ticks_frame


def resample_df(df, interval, currency_name, save_csv=True):
    df['time'] = pd.to_datetime(df['time'])
    # ticks_frame = df.set_index(df['time'])
    # data_ask = ticks_frame['ask'].resample(interval).ohlc()
    # data_bid = ticks_frame['bid'].resample(interval).ohlc()
    # data_ask.fillna(data_ask.mean())
    # data_bid.fillna(data_bid.mean())

    # data = pd.DataFrame()
    # data['open'] = (data_ask['open'] + data_bid['open']) / 2
    # data['high'] = (data_ask['high'] + data_bid['high']) / 2
    # data['low'] = (data_ask['low'] + data_bid['low']) / 2
    # data['close'] = (data_ask['close'] + data_bid['close']) / 2
    # data = data.reset_index()

    data = df.fillna(df.mean(numeric_only=True))

    if save_csv:
        folder_name = 'dataset'
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        data.to_csv(f"{folder_name}" + os.sep + f"{interval}_{currency_name}.csv")
    mt5.shutdown()

    return data


# currency = 'EURUSD'
# raw_data_df = get_data_mt5(currency)
# print(resample_df(raw_data_df, '1Min', currency, save_csv=False).tail())
