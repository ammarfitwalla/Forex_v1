import os
import numpy as np
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from silence_tensorflow import silence_tensorflow

silence_tensorflow()
from tensorflow.keras.layers import Dense
from tensorflow_core.python.keras.layers import Activation
from tensorflow.keras.models import Sequential, load_model
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM, ConvLSTM2D, Input

def train_model(x_train, y_train, save_name):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.1))
    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.1))
    # model.add(LSTM(50, return_sequences=True))
    # model.add(Dropout(0.1))
    # model.add(LSTM(128, return_sequences=True))
    # model.add(Dropout(0.1))
    # model.add(LSTM(64, return_sequences=True))
    # model.add(Dropout(0.2))
    model.add(LSTM(64))
    # model.add(Dropout(0.1))
    model.add(Dense(units=y_train.shape[1]))
    # model.add(Activation('linear'))

    model.compile(loss='mean_squared_error', optimizer='adam')
    history = model.fit(x_train, y_train, epochs=2, batch_size=32, verbose=1, validation_split=0.3)
    model.summary()
    model.save(save_name)

    plt.plot(history.history['loss'], label='training loss')
    plt.plot(history.history['val_loss'], label='validation loss')
    plt.legend()
    plt.show()
    return model


def get_forecast_df(model, x_train, n_future, train_set, sc, col_ind, forecast_period_dates, col_name):
    forecast = model.predict(x_train[-n_future:])
    forecast_copies = np.repeat(forecast, train_set.shape[1], axis=-1)
    y_pred_future = sc.inverse_transform(forecast_copies)[:, col_ind]

    forecast_dates = []
    for time_i in forecast_period_dates:
        forecast_dates.append(time_i)

    df_forecast = pd.DataFrame({'time': np.array(forecast_dates), col_name: y_pred_future})
    df_forecast['time'] = pd.to_datetime(df_forecast['time'])
    return df_forecast


class XLocIndexer:
    def __init__(self, frame):
        self.frame = frame

    def __getitem__(self, key):
        row, col = key
        return self.frame.iloc[row][col]


# pd.core.indexing.IndexingMixin.xloc = property(lambda frame: XLocIndexer(frame))

def split_data(scaled_data, n_future, n_past, col_index):
    x_train = []
    y_train = []

    for x in range(n_past, len(scaled_data) - n_future + 1):
        x_train.append(scaled_data[x - n_past:x, 0:scaled_data.shape[1]])
        y_train.append(scaled_data[x + n_future - 1:x + n_future, col_index])

    return x_train, y_train


def get_model(df, interval, currency_name, n_past, n_future):
    base_folder = 'trained_models'
    current_model_folder_name = f'{interval}_{currency_name}'

    # current_model_folder_name = os.path.join(base_folder, f'{interval}_{currency_name}')

    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)

    if not os.path.isdir(os.path.join(base_folder, current_model_folder_name)):
        os.mkdir(os.path.join(base_folder, current_model_folder_name))
        os.mkdir(os.path.join(base_folder, current_model_folder_name, 'high_models'))
        os.mkdir(os.path.join(base_folder, current_model_folder_name, 'low_models'))

    high_model_save_path = os.path.join(base_folder, current_model_folder_name, 'high_models', 'high.h5')
    low_model_save_path = os.path.join(base_folder, current_model_folder_name, 'low_models', 'low.h5')
    df = df.drop(range(0, 100), axis=0)

    cols = ['high', 'low', 'RSI_HLCC/4', 'MA_Slow_HLCC/4', 'MA_Fast_HLCC/4']

    train_set = df[cols].astype(float)

    sc = StandardScaler()
    scaled_data = sc.fit_transform(train_set)

    high_x_train, high_y_train = split_data(scaled_data, n_future, n_past, 0)
    low_x_train, low_y_train = split_data(scaled_data, n_future, n_past, 1)

    high_x_train, high_y_train = np.array(high_x_train), np.array(high_y_train)
    print("high x_train shape:", high_x_train.shape)
    print("high y_train shape:", high_y_train.shape)

    low_x_train, low_y_train = np.array(low_x_train), np.array(low_y_train)
    print("low x_train shape:", low_x_train.shape)
    print("low y_train shape:", low_y_train.shape)

    """
    training of models
    """
    high_model = train_model(
        high_x_train,
        high_y_train,
        high_model_save_path)

    low_model = train_model(
        low_x_train,
        low_y_train,
        low_model_save_path)

    return high_model, low_model

    # """
    # loading saved model
    # """
    # high_new_model_path = high_model_save_path
    # high_new_model = load_model(high_new_model_path)
    #
    # low_new_model_path = low_model_save_path
    # low_new_model = load_model(low_new_model_path)
    #
    # # Forecasting...
    # # Start with the last day in training date and predict future...
    # n_future = 3000  # Redefining n_future to extend prediction dates beyond original n_future dates...
    # print(list(train_dates)[-1])
    # forecast_period_dates = pd.date_range(list(train_dates)[-3000], periods=n_future, freq='1min').tolist()
    # print(forecast_period_dates)
    #
    # # def get_forecast_df(model, x_train, n_future, train_set, sc, col_ind, forecast_period_dates, col_name):
    # high_df_forecast = get_forecast_df(high_new_model, high_x_train, n_future, train_set, sc, 0, forecast_period_dates,
    #                                    'high')
    # print("high")
    # print(high_df_forecast)
    # high_df_forecast.to_csv("1min_high_df_pred.csv")
    # low_df_forecast = get_forecast_df(low_new_model, low_x_train, n_future, train_set, sc, 1, forecast_period_dates,
    #                                   'low')
    # print("low")
    # print(low_df_forecast)
    # low_df_forecast.to_csv("1min_low_df_pred.csv")
