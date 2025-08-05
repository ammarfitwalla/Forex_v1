# models.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from db_connection import Base

class Prediction(Base):
    __tablename__ = "forex_app_prediction"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timeframe = Column(String)
    forecast_time = Column(DateTime)
    high_forecast = Column(Float)
    low_forecast = Column(Float)
    last_open = Column(Float, nullable=True)
    last_high = Column(Float, nullable=True)
    last_low = Column(Float, nullable=True)
    last_close = Column(Float, nullable=True)
    high_rsi = Column(Float)
    low_rsi = Column(Float)
    high_sma = Column(Float)
    high_fma = Column(Float)
    low_sma = Column(Float)
    low_fma = Column(Float)
    created_at = Column(DateTime, nullable=False)
    actual_high = Column(Float, nullable=True)
    actual_low = Column(Float, nullable=True)
    actual_open = Column(Float, nullable=True)
    actual_close = Column(Float, nullable=True)

