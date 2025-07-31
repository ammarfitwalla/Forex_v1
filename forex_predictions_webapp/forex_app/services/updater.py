from datetime import datetime
from .mt5_utils import get_data_mt5
from forex_app.models import Prediction

def update_actuals(symbol='EURUSD', timeframe='5Min'):
    # Get pending predictions (actual still NULL)
    pending = Prediction.objects.filter(symbol=symbol, timeframe=timeframe, actual_open__isnull=True)

    if not pending.exists():
        return

    df = get_data_mt5(symbol, timeframe)
    if df is None or df.empty:
        return

    for pred in pending:
        # Find candle that matches forecast_time
        actual_candle = df.loc[df['time'] == pred.forecast_time]
        if not actual_candle.empty:
            candle = actual_candle.iloc[0]
            pred.actual_open = candle['open']
            pred.actual_high = candle['high']
            pred.actual_low = candle['low']
            pred.actual_close = candle['close']
            pred.save()
