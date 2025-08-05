# main.py

from app.services.scheduler import start_scheduler

if __name__ == "__main__":
    start_scheduler()
    print("[Main] Scheduler started. Running predictions every 5 minutes.")
    # The scheduler will run in the background, so the script will keep running.