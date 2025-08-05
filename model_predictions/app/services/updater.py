from datetime import datetime
from app.utils.mt5_utils import get_data_mt5
from sqlalchemy.orm import Session
from app.db.db_connection import SessionLocal
from app.db.orm_models import Prediction

# Threshold to decide whether the prediction was met or missed (in pips)
THRESHOLD_PIPS = 5.0

# Maximum tolerable error in pips for scaling the accuracy score
MAX_TOLERANCE_PIPS = 20.0

def calculate_accuracy(error_pips: float) -> float:
    """
    Returns an accuracy score between 0 and 100 based on error.
    Score decreases linearly as error increases up to MAX_TOLERANCE_PIPS.
    """
    return max(0.0, 100.0 - (error_pips / MAX_TOLERANCE_PIPS) * 100.0)

def update_actuals(symbol, actual_high, actual_low, actual_open, actual_close, last_time):
    # Start a new SQLAlchemy session
    db: Session = SessionLocal()

    # Get predictions for which actuals are not yet recorded
    pending = db.query(Prediction).filter(
        Prediction.symbol == symbol,
        Prediction.forecast_time == last_time,
        Prediction.actual_open == None
    ).all()

    if not pending:
        db.close()
        print(f"[Updater] No pending predictions for {symbol} at {last_time}")
        return

    for prediction in pending:
        # Set actual values
        prediction.actual_open = actual_open
        prediction.actual_high = actual_high
        prediction.actual_low = actual_low
        prediction.actual_close = actual_close

        # --- Calculate error in pips ---
        # Multiply by 10,000 for 4-digit pairs (e.g., EURUSD)
        high_error_pips = abs(actual_high - prediction.high_forecast) * 10000
        low_error_pips = abs(actual_low - prediction.low_forecast) * 10000

        prediction.high_error_pips = high_error_pips
        prediction.low_error_pips = low_error_pips

        # --- Calculate accuracy score based on error ---
        prediction.high_accuracy_score = calculate_accuracy(high_error_pips)
        prediction.low_accuracy_score = calculate_accuracy(low_error_pips)

        # --- Determine if prediction was met or missed based on threshold ---
        # If actual price meets or exceeds the forecast threshold, mark as 'met'
        prediction.met_or_missed_high = (
            'met' if actual_high >= (prediction.high_forecast - THRESHOLD_PIPS / 10000) else 'missed'
        )

        # If actual price falls below or matches low forecast threshold, mark as 'met'
        prediction.met_or_missed_low = (
            'met' if actual_low <= (prediction.low_forecast + THRESHOLD_PIPS / 10000) else 'missed'
        )

    # Commit the updates to the database
    db.commit()
    db.close()

    print(f"[Updater] Updated actuals + accuracy for {len(pending)} predictions for {symbol} at {last_time}")
