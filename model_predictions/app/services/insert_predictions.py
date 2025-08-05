# insert_prediction.py

from sqlalchemy.orm import Session
from datetime import datetime
from app.db.db_connection import SessionLocal
from app.db.orm_models import Prediction

# Function to insert prediction data into the database
def insert_prediction_to_db(symbol, timeframe, forecast_time, high_forecast, low_forecast, last_candle):
    # Create a new session
    db: Session = SessionLocal()

    try:
        # Create a new Prediction object
        prediction = Prediction(
            symbol=symbol,
            timeframe=timeframe,
            forecast_time=forecast_time,
            high_forecast=high_forecast,
            low_forecast=low_forecast,
            high_rsi=last_candle.get('high_rsi'),
            low_rsi=last_candle.get('low_rsi'),
            high_sma=last_candle.get('high_sma'),
            high_fma=last_candle.get('high_fma'),
            low_sma=last_candle.get('low_sma'),
            low_fma=last_candle.get('low_fma'),
            actual_high=None,  # actual values will be updated later
            actual_low=None,    # actual values will be updated later
            actual_open=None,
            actual_close=None,
            created_at=datetime.utcnow()  # Set the creation time
        )

        # Add the prediction object to the session
        db.add(prediction)

        # Commit the transaction to insert the data
        db.commit()

        print(f"Prediction inserted successfully for {symbol} at {forecast_time}")
        
    except Exception as e:
        print(f"Error inserting prediction into DB: {e}")
        db.rollback()  # Rollback the transaction on error
    
    finally:
        db.close()  # Close the session