import os
import time
import pytz
import numpy as np
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta
from silence_tensorflow import silence_tensorflow
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from urllib.parse import quote
silence_tensorflow()


model = load_model(r'D:\UpWork\Projects\Forex_v1\model_training_codes\trained_models\3H_USDJPY\high_models\high.h5', compile=False)
print(model.summary())