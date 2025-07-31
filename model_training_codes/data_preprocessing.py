import os


def get_rsi(file, value, n):
    """
    calculates -> RSI value
    takes argument -> dataframe, column name, period value
    returns dataframe by adding column :  column name + '_rsi'
    """
    delta = file[value].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(span=n, adjust=False).mean()
    ema_down = down.ewm(span=n, adjust=False).mean()
    rs = ema_up / ema_down
    file[value+'_rsi'] = 100 - (100 / (1 + rs))

    return file


def moving_avg(ultratech_df, value, slow_p, fast_p, slow_ma_col_name, fast_ma_col_name):
    """
    calculates -> slow moving average, fast moving average
    takes argument -> dataframe, column name, slow period, fast period
    returns dataframe by adding columns -> 'MA_Slow_HLCC/4',  'SMA_period', MA_Fast_HLCC/4', 'FMA_period'
    """

    ultratech_df[slow_ma_col_name] = ultratech_df[value].rolling(window=slow_p, min_periods=1).mean()
    ultratech_df[f'{slow_ma_col_name}_period'] = slow_p
    ultratech_df[fast_ma_col_name] = ultratech_df[value].rolling(window=fast_p, min_periods=1).mean()
    ultratech_df[f'{fast_ma_col_name}_period'] = fast_p

    return ultratech_df


def get_preprocessed_data(df, save_df_to_csv=False, csv_file_path=None):
    """
    > adding a column in dataframe: HLCC/4,  with formula : (high * low * close * close) / 4
       NOTE: high, low, close are columns in dataframe
    """
    # # =================== HLCC =================== # #
    # df['HLCC/4'] = (df['high'] + df['low'] + df['close'] + df['close']) / 4
    # with_rsi_df = get_rsi(df, 'HLCC/4', 14)
    # with_mov_avg = moving_avg(with_rsi_df, 'HLCC/4', 17, 7)

    # if save_df:
    #     folder_name = 'preprocessed_csv'
    #     if not os.path.isdir(folder_name):
    #         os.mkdir(folder_name)
    #     with_mov_avg.to_csv(f"{folder_name}" + os.sep + "preprocessed.csv")

    # =================== HIGH & LOW =================== #

    with_high_rsi_df = get_rsi(df, 'high', 14)
    with_low_rsi_df = get_rsi(with_high_rsi_df, 'low', 14)

    with_high_mov_avg = moving_avg(ultratech_df=with_low_rsi_df, value='high', slow_p=17, fast_p=7,
                                                    slow_ma_col_name='high_sma', fast_ma_col_name='high_fma')

    with_low_mov_avg = moving_avg(ultratech_df=with_high_mov_avg, value='low', slow_p=17, fast_p=7,
                                                    slow_ma_col_name='low_sma', fast_ma_col_name='low_fma')

    if save_df_to_csv:
        with_low_mov_avg.to_csv(csv_file_path)

    return with_low_mov_avg
