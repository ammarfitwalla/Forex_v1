import os
from app.services.insert_predictions import insert_prediction_to_db
from app.services.updater import update_actuals
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN optimizations

import numpy as np
import pandas as pd
from utils.mt5_utils import get_data_yf
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# Load models (SavedModel format, .pb inside folder "1/")
print(os.getcwd())

# Path to SavedModel directories (export_dir/1/)
high_model_dir = r'D:\UpWork\Projects\Forex_v1\high_model_dir\1'
low_model_dir = r'D:\UpWork\Projects\Forex_v1\low_model_dir\1'

high_model = tf.saved_model.load(high_model_dir)
low_model = tf.saved_model.load(low_model_dir)

# Get the callable serving function
high_infer = high_model.signatures["serving_default"]
low_infer = low_model.signatures["serving_default"]

def run_prediction(symbol='EURUSD', timeframe='5Min'):
    df = get_data_yf(symbol+"=X", '5m')
    print(df.tail())
    print(df.columns.to_list())
    if df is None or df.empty:
        print("No data fetched from MT5")
        return None

    high_scaler = StandardScaler()
    low_scaler = StandardScaler()

    cols = ['High', 'High_rsi', 'high_sma', 'high_fma']
    high_scaled = high_scaler.fit_transform(df[cols])
    low_scaled = low_scaler.fit_transform(df[['Low', 'Low_rsi', 'low_sma', 'low_fma']])

    N_FUTURE, N_PAST = 1, 48
    x_high = np.array([high_scaled[-N_PAST:]], dtype=np.float32)
    x_low = np.array([low_scaled[-N_PAST:]], dtype=np.float32)

    # Predict using SavedModel
    high_pred_tensor = high_infer(tf.constant(x_high))
    low_pred_tensor = low_infer(tf.constant(x_low))

    # Extract prediction from the dictionary output
    high_forecast_scaled = list(high_pred_tensor.values())[0].numpy()[0][0]
    low_forecast_scaled = list(low_pred_tensor.values())[0].numpy()[0][0]

    print(f"[Predictor] High forecast scaled: {high_forecast_scaled}")
    print(f"[Predictor] Low forecast scaled: {low_forecast_scaled}")

    # Inverse transform
    high_forecast = high_scaler.inverse_transform([[high_forecast_scaled, 0, 0, 0]])[0][0]
    low_forecast = low_scaler.inverse_transform([[low_forecast_scaled, 0, 0, 0]])[0][0]
    print(f"[Predictor] High forecast (original scale): {high_forecast}")
    print(f"[Predictor] Low forecast (original scale): {low_forecast}")

    last_time = df['Datetime'].iloc[-1]
    forecast_time = last_time + pd.to_timedelta(timeframe)
    last_candle = df.iloc[-1].to_dict()

    print(f"[Predictor] Forecast for {symbol} at {forecast_time}: high={high_forecast}, low={low_forecast}")

    update_actuals(
        symbol=symbol,
        actual_high=last_candle['High'],
        actual_low=last_candle['Low'],
        actual_open=last_candle['Open'],
        actual_close=last_candle['Close'],
        last_time=last_time
    )

    insert_prediction_to_db(
        symbol=symbol,
        timeframe=timeframe,
        forecast_time=forecast_time,
        high_forecast=float(high_forecast),
        low_forecast=float(low_forecast),
        last_candle=last_candle
    )


# run_prediction(symbol='EURUSD', timeframe='5Min')