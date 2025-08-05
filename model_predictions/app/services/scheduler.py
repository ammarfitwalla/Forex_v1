import threading
from datetime import datetime
from app.predictor import run_prediction
import time
import sys

INTERVAL = 5  # minutes
scheduler_timer = None  # Global reference to allow cleanup

def is_forex_market_open():
    """Check if the forex market is open (Mon-Fri)"""
    now = datetime.utcnow()
    weekday = now.weekday()  # Monday=0, Sunday=6
    return weekday not in [5, 6]

def scheduled_job():
    """The job that runs at a fixed interval"""
    global scheduler_timer
    print(f"[Scheduler] Running job at {datetime.now()}")

    if is_forex_market_open():
        try:
            run_prediction(symbol='EURUSD', timeframe='5Min')
        except Exception as e:
            print(f"[Scheduler] Error running prediction: {e}")
    else:
        print("[Scheduler] Forex market closed, skipping prediction & update.")
    
    # Schedule the next run
    scheduler_timer = threading.Timer(INTERVAL * 60, scheduled_job)
    scheduler_timer.start()

def start_scheduler():
    """Start the scheduler and handle graceful shutdown"""
    print("[Scheduler] Starting job scheduler...")
    try:
        scheduled_job()  # Start the first job
        while True:
            time.sleep(1)  # Keeps the main thread alive to handle Ctrl+C
    except KeyboardInterrupt:
        print("\n[Scheduler] Scheduler interrupted. Exiting gracefully...")
        stop_scheduler()
        sys.exit(0)

def stop_scheduler():
    """Stop the timer if it's running"""
    global scheduler_timer
    if scheduler_timer is not None:
        scheduler_timer.cancel()
        print("[Scheduler] Timer stopped.")
    else:
        print("[Scheduler] No timer to stop.")