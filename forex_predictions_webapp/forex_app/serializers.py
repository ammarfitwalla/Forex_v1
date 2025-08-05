from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    # Custom field for formatted forecast time
    formatted_forecast_time = serializers.DateTimeField(source='forecast_time', format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Prediction
        fields = [
            'id',
            'symbol',
            'timeframe',
            'forecast_time',
            'formatted_forecast_time',  # Custom formatted field
            'high_forecast',
            'low_forecast',
            'actual_high',
            'actual_low',
            'last_open',
            'last_high',
            'last_low',
            'last_close',
            'high_rsi',
            'low_rsi',
            'high_sma',
            'high_fma',
            'low_sma',
            'low_fma',
            'met_or_missed_high',
            'met_or_missed_low',
            'high_accuracy_score',
            'low_accuracy_score',
        ]
        read_only_fields = ['id', 'formatted_forecast_time']  # Making 'id' and 'formatted_forecast_time' read-only
        extra_kwargs = {
            'forecast_time': {'format': '%Y-%m-%d %H:%M:%S'}  # Ensure forecast_time is formatted correctly
        }