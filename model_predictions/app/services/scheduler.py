import threading
from datetime import datetime
from app.predictor import run_prediction

INTERVAL = 5  # minutes

def is_forex_market_open():
    now = datetime.utcnow()
    weekday = now.weekday()  # Monday=0 ... Sunday=6
    return weekday not in [5, 6]

def scheduled_job():
    print(f"[Scheduler] Running job at {datetime.now()}")
    if is_forex_market_open():
        run_prediction(symbol='EURUSD', timeframe='5Min')
    else:
        print("[Scheduler] Forex market closed, skipping prediction & update.")
    
    # Schedule the next run after the interval
    threading.Timer(INTERVAL * 60, scheduled_job).start()

def start_scheduler():
    scheduled_job()