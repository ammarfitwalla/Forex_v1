import os
import pandas as pd
from training_LSTM_models import get_model
from get_data import get_data_mt5, resample_df
from data_preprocessing import get_preprocessed_data

CURRENCY_NAME = 'EURUSD'
DATASET_YEARS = '4Y'
INTERVAL = '5M'
FILE_PATH = r"D:\UpWork\Projects\Forex_v1\currency_datasets\EURUSD\4Y_5M\EURUSD_M5.csv" #f'../currency_datasets/{CURRENCY_NAME}/{DATASET_YEARS}_{INTERVAL}/{CURRENCY_NAME}_{INTERVAL}.csv'

preprocessed_csv_file_path = f'preprocessed_csv{os.sep}{CURRENCY_NAME}_{DATASET_YEARS}_{INTERVAL}_preprocessed.csv'

# df = get_data_mt5(CURRENCY_NAME)

df = pd.read_csv(FILE_PATH)
# print(len(df))

# df.rename(columns={'Time': 'time', 'Bid': 'bid', 'Ask': 'ask'}, inplace=True)
# df.to_csv(f'../currency_datasets/{CURRENCY_NAME}/{DATASET_YEARS}/{CURRENCY_NAME}_mt5_ticks_v1.csv')

resampled_df = resample_df(df, INTERVAL, CURRENCY_NAME, save_csv=False)
preprocessed_df = get_preprocessed_data(resampled_df, save_df_to_csv=True, csv_file_path=preprocessed_csv_file_path)
# preprocessed_df = pd.read_csv(preprocessed_csv_file_path)

high_model, low_model = get_model(preprocessed_df, INTERVAL, CURRENCY_NAME, n_past=48, n_future=1)
