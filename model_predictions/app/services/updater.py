from datetime import datetime
from app.utils.mt5_utils import get_data_mt5
from sqlalchemy.orm import Session
from app.db.db_connection import SessionLocal
from app.db.orm_models import Prediction

def update_actuals(symbol, actual_high, actual_low, actual_open, actual_close, last_time):
    # Start a new session
    db: Session = SessionLocal()

    # Get pending predictions (actual_* = NULL)
    pending = db.query(Prediction).filter(
        Prediction.symbol == symbol,
        Prediction.forecast_time == last_time,
        Prediction.actual_open == None
    ).all()

    if not pending:
        db.close()
        print(f"[Updater] No pending predictions for {symbol} at {last_time}")
        return

    # Update each prediction
    for prediction in pending:
        prediction.actual_open = actual_open
        prediction.actual_high = actual_high
        prediction.actual_low = actual_low
        prediction.actual_close = actual_close

    # Commit the update to the database
    db.commit()
    db.close()

    print(f"[Updater] Updated actual values for {len(pending)} predictions for {symbol} at {last_time}")
