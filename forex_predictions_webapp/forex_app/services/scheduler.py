import os
import threading
from datetime import datetime
from .predictor import run_prediction
from .updater import update_actuals

INTERVAL = 5  # minutes
SCHEDULER_RUNNING = False
SCHEDULER_LOCK = threading.Lock()

def is_forex_market_open():
    now = datetime.utcnow()
    weekday = now.weekday()  # Monday=0 ... Sunday=6
    return weekday not in [5, 6]

def scheduled_job():
    # Use the lock to ensure no overlapping runs
    with SCHEDULER_LOCK:
        print(f"[Scheduler] Running job at {datetime.now()}")
        if is_forex_market_open():
            run_prediction(symbol='EURUSD', timeframe='5Min')
            # Uncomment this line if you want to update actual values
            # update_actuals(symbol='EURUSD', timeframe='5Min')
        else:
            print("[Scheduler] Forex market closed, skipping prediction & update.")
        
    # Schedule the next run after the interval
    threading.Timer(INTERVAL * 60, scheduled_job).start()

def start_scheduler():
    global SCHEDULER_RUNNING
    if SCHEDULER_RUNNING:
        print("[Scheduler] Already running, skipping duplicate start.")
        return
    
    SCHEDULER_RUNNING = True
    print("[Scheduler] Starting prediction scheduler...")
    scheduled_job()

# Only start in the main process (avoid Django auto-reloader duplication)
if os.environ.get('RUN_MAIN') == 'true':
    start_scheduler()
    print("[Scheduler] Scheduler started successfully.")
else:
    print("[Scheduler] Not starting scheduler in non-main process.")
