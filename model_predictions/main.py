# main.py

from app.services.scheduler import start_scheduler  # or whatever the main function is

if __name__ == "__main__":
    print("Starting Forex AI System...")
    start_scheduler()
    print("Scheduler started successfully.")
    # The scheduler will run indefinitely, so no need for a loop here.