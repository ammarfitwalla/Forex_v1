from django.db import models

from django.db import models

class Prediction(models.Model):
    # --- Metadata ---
    symbol = models.CharField(max_length=10)        
    timeframe = models.CharField(max_length=10)     
    forecast_time = models.DateTimeField()          

    # --- Prediction output ---
    high_forecast = models.FloatField()
    low_forecast = models.FloatField()

    # --- Last observed candle (input candle) ---
    last_open = models.FloatField(null=True, blank=True)
    last_high = models.FloatField(null=True, blank=True)
    last_low = models.FloatField(null=True, blank=True)
    last_close = models.FloatField(null=True, blank=True)

    # --- Indicators ---
    high_rsi = models.FloatField(null=True, blank=True)
    low_rsi = models.FloatField(null=True, blank=True)
    high_sma = models.FloatField(null=True, blank=True)
    high_fma = models.FloatField(null=True, blank=True)
    low_sma = models.FloatField(null=True, blank=True)
    low_fma = models.FloatField(null=True, blank=True)

    # --- Actual outcome (future candle predicted) ---
    actual_open = models.FloatField(null=True, blank=True)
    actual_high = models.FloatField(null=True, blank=True)
    actual_low = models.FloatField(null=True, blank=True)
    actual_close = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} {self.timeframe} {self.forecast_time}"

