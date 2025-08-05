import os
# os['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # Disable oneDNN optimizations

import numpy as np
import pandas as pd
from mt5_utils import get_data_mt5   # function that fetches candles from MT5
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
# from models import Prediction
from updater import update_actuals
from insert_predictions import insert_prediction_to_db

# Load trained models once (avoid reloading every prediction)
print(os.getcwd())

high_model = load_model('ml_models'+os.sep+'high_models'+os.sep+'high.h5')
low_model = load_model('ml_models'+os.sep+'low_models'+os.sep+'low.h5')
# low_model = load_model(r'../ml_models/low_models/low.h5')

def run_prediction(symbol='EURUSD', timeframe='5Min'):
    df = get_data_mt5(symbol, timeframe)
    if df is None or df.empty:
        print("No data fetched from MT5")
        return None

    # Step 1: Create the scalers for high and low values
    # Step 1: Create scalers
    high_scaler = StandardScaler()
    low_scaler = StandardScaler()

    # Step 2: Scale the data using StandardScaler (fit and transform)
    cols = ['high', 'high_rsi', 'high_sma', 'high_fma']
    high_scaled = high_scaler.fit_transform(df[cols])  # Fit and transform on high data
    low_scaled = low_scaler.fit_transform(df[['low', 'low_rsi', 'low_sma', 'low_fma']])  # Fit and transform on low data

    N_FUTURE, N_PAST = 1, 48
    x_high = [high_scaled[-N_PAST:]]
    x_low = [low_scaled[-N_PAST:]]

    # Step 3: Make predictions (scaled data)
    high_forecast_scaled = high_model.predict(np.array(x_high))[0][0]
    low_forecast_scaled = low_model.predict(np.array(x_low))[0][0]

    # Step 4: Inverse the transformation for high forecast (to get the original scale)
    # Use inverse_transform after the scaler has been fitted
    high_forecast = high_scaler.inverse_transform([[high_forecast_scaled, 0, 0, 0]])[0][0]

    # Step 5: Inverse the transformation for low forecast (to get the original scale)
    low_forecast = low_scaler.inverse_transform([[low_forecast_scaled, 0, 0, 0]])[0][0]

    # # Printing the results
    # print(f"High Forecast (original scale): {high_forecast_original}")
    # print(f"Low Forecast (original scale): {low_forecast_original}")


    # Next candle time
    last_time = df['time'].iloc[-1]
    forecast_time = last_time + pd.to_timedelta(timeframe)

    # Last candle snapshot (input candle)
    last_candle = df.iloc[-1].to_dict()

    print(f"[Predictor] Forecast for {symbol} at {forecast_time}: high={high_forecast}, low={low_forecast}")

    update_actuals(symbol=symbol,
                   actual_high=last_candle['high'],
                   actual_low=last_candle['low'],
                   actual_open=last_candle['open'],
                   actual_close=last_candle['close'],
                   last_time=last_time)

    insert_prediction_to_db(
        symbol=symbol,
        timeframe=timeframe,
        forecast_time=forecast_time,
        high_forecast=float(high_forecast),
        low_forecast=float(low_forecast),
        last_candle=last_candle
    )

    # Insert new prediction row (actual_* = NULL initially)
    # prediction = Prediction.objects.create(
    #     symbol=symbol,
    #     timeframe=timeframe,
    #     forecast_time=forecast_time,
    #     high_forecast=float(high_forecast),
    #     low_forecast=float(low_forecast),
    #     # last_open=last_candle['open'],
    #     # last_high=last_candle['high'],
    #     # last_low=last_candle['low'],
    #     # last_close=last_candle['close'],
    #     high_rsi=last_candle.get('high_rsi'),
    #     low_rsi=last_candle.get('low_rsi'),
    #     high_sma=last_candle.get('high_sma'),
    #     high_fma=last_candle.get('high_fma'),
    #     low_sma=last_candle.get('low_sma'),
    #     low_fma=last_candle.get('low_fma'),
    #     # actual_* stays NULL
    # )

    # return prediction

# def update_actual_values(symbol, actual_high, actual_low, actual_open, actual_close, last_time):
#     """ Update actual values in the latest prediction row
#     """
#     # Find the most recent prediction where actuals are still NULL
#     prediction = Prediction.objects.filter(
#         symbol=symbol,
#         forecast_time=last_time,
#         actual_high__isnull=True, 
#         actual_low__isnull=True
#     ).first()

#     if prediction:
#         # Update with actual high and low values
#         prediction.actual_high = actual_high
#         prediction.actual_low = actual_low
#         prediction.actual_open = actual_open
#         prediction.actual_close = actual_close
#         prediction.save()

#         print(f"Updated actuals for {symbol} at {prediction.forecast_time}: high={actual_high}, low={actual_low}")
#         print(f"Open={actual_open}, Close={actual_close}")
#     else:
#         print(f"No prediction row found to update for {symbol}.")
