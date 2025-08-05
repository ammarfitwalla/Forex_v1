# import MetaTrader5 as mt5
# import numpy as np
# import pandas as pd
# from datetime import datetime, timedelta
# import pytz


# def next_weekday(d, weekday):
#     days_ahead = weekday - d.weekday()
#     if days_ahead <= 0:  # Target day already happened this week
#         days_ahead += 7
#     return d + timedelta(days_ahead)


# def get_rsi(file, value, n):
#     """
#     calculates -> RSI value
#     takes argument -> dataframe, column name, period value
#     returns dataframe by adding column :  column name + '_rsi'
#     """
#     delta = file[value].diff()
#     up = delta.clip(lower=0)
#     down = -1 * delta.clip(upper=0)
#     ema_up = up.ewm(span=n, adjust=False).mean()
#     ema_down = down.ewm(span=n, adjust=False).mean()
#     rs = ema_up / ema_down
#     file[value + '_rsi'] = 100 - (100 / (1 + rs))

#     return file


# def moving_avg(ultratech_df, value, slow_p, fast_p, slow_ma_col_name, fast_ma_col_name):
#     """
#     calculates -> slow moving average, fast moving average
#     takes argument -> dataframe, column name, slow period, fast period
#     returns dataframe by adding columns -> 'MA_Slow_HLCC/4',  'SMA_period', MA_Fast_HLCC/4', 'FMA_period'
#     """

#     ultratech_df[slow_ma_col_name] = ultratech_df[value].rolling(window=slow_p, min_periods=1).mean()
#     ultratech_df[f'{slow_ma_col_name}_period'] = slow_p
#     ultratech_df[fast_ma_col_name] = ultratech_df[value].rolling(window=fast_p, min_periods=1).mean()
#     ultratech_df[f'{fast_ma_col_name}_period'] = fast_p

#     return ultratech_df


# def get_forecast_df(train_set, model, x_train, col_ind, col_name, N_FUTURE, sc, forecast_period_dates):
#     """
#     returns next prediction in a dataframe
#     """
#     forecast = model.predict(x_train[-N_FUTURE:])  # forecast
#     forecast_copies = np.repeat(forecast, train_set.shape[1], axis=-1)
#     y_pred_future = sc.inverse_transform(forecast_copies)[:, col_ind]
#     forecast_dates = []
#     for time_i in forecast_period_dates:
#         forecast_dates.append(time_i)

#     df_forecast = pd.DataFrame({'time': np.array(forecast_dates), col_name: y_pred_future})
#     df_forecast['time'] = pd.to_datetime(df_forecast['time'])

#     return df_forecast


# def get_data_mt5(currency_name, interval):
#     if not mt5.initialize():
#         print("initialize() failed, error code =", mt5.last_error())
#         return None
#     try:
#         utc_from = datetime.now(tz=pytz.utc) - timedelta(days=150)
#         utc_to = datetime.now(tz=pytz.utc)

#         ticks = mt5.copy_ticks_range(currency_name, utc_from, utc_to, mt5.COPY_TICKS_ALL)
#         ticks_frame = pd.DataFrame(ticks)
#         ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
#         ticks_frame = ticks_frame.set_index(ticks_frame['time'])
#         data_ask = ticks_frame['ask'].resample(interval).ohlc()
#         data_bid = ticks_frame['bid'].resample(interval).ohlc()
#         data = pd.DataFrame()
#         data['open'] = (data_ask['open'] + data_bid['open']) / 2
#         data['high'] = (data_ask['high'] + data_bid['high']) / 2
#         data['low'] = (data_ask['low'] + data_bid['low']) / 2
#         data['close'] = (data_ask['close'] + data_bid['close']) / 2
#         data = data.reset_index()

#         data = get_rsi(data, 'high', 14)
#         data = get_rsi(data, 'low', 14)

#         data = moving_avg(ultratech_df=data, value='high', slow_p=17, fast_p=7, slow_ma_col_name='high_sma', fast_ma_col_name='high_fma')

#         data = moving_avg(ultratech_df=data, value='low', slow_p=17, fast_p=7, slow_ma_col_name='low_sma', fast_ma_col_name='low_fma')
#         data = data.fillna(data.mean(numeric_only=True))
#         data = data.tail(5000)
#         mt5.shutdown()
#         return data
#     except:
#         return None