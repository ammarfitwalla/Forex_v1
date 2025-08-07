from django.shortcuts import render
from django.db.models import Avg

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Prediction
from .serializers import PredictionSerializer
from rest_framework.pagination import PageNumberPagination


class PredictionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def latest_predictions(request):
    paginator = PredictionPagination()
    predictions = Prediction.objects.all().order_by('-forecast_time')[:50]
    result_page = paginator.paginate_queryset(predictions, request)
    serializer = PredictionSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def prediction_by_symbol(request, symbol):
    predictions = Prediction.objects.filter(symbol=symbol).order_by('-forecast_time')[:100]
    serializer = PredictionSerializer(predictions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filtered_predictions(request):
    # Get query parameters
    symbol = request.query_params.get('symbol', None)
    start_date = request.query_params.get('start_date', None)
    end_date = request.query_params.get('end_date', None)
    
    predictions = Prediction.objects.all()

    if symbol:
        predictions = predictions.filter(symbol=symbol)
    if start_date and end_date:
        predictions = predictions.filter(forecast_time__range=[start_date, end_date])
    
    predictions = predictions.order_by('-forecast_time')[:50]
    serializer = PredictionSerializer(predictions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def accuracy_summary(request):
    symbols = Prediction.objects.values_list('symbol', flat=True).distinct()
    print(f"[Summary] Found {len(symbols)} unique symbols for accuracy summary")
    if not symbols:
        return Response({"summary": []})

    summary = []
    # Print debug information
    print(f"[Summary] Generating accuracy summary for {len(symbols)} symbols")
    # Iterate through each unique symbol to calculate summary metrics
    for symbol in symbols:
        print(f"[Summary] Processing symbol: {symbol}")
        qs = Prediction.objects.filter(symbol=symbol).order_by('-forecast_time')[:100]
        
        print(f"[Summary] Processing symbol: {symbol}, total predictions: {qs.count()}")

        if not qs.exists():
            print(f"[Summary] No predictions found for symbol: {symbol}")
            continue

        print(f"[Summary] Processing symbol: {symbol}, total predictions: {qs.count()}")

        # Calculate summary metrics
        total = qs.count()
        if total == 0:
            continue
        qs_list = list(qs)  # Force evaluation

        # Count manually
        high_met = sum(1 for q in qs_list if q.met_or_missed_high == 'met')
        low_met = sum(1 for q in qs_list if q.met_or_missed_low == 'met')

        print(f"[Summary] High met: {high_met}, Low met: {low_met} for symbol: {symbol}")

        # Calculate average accuracy scores
        high_accuracy_scores = [q.high_accuracy_score for q in qs_list if q.high_accuracy_score is not None]
        low_accuracy_scores = [q.low_accuracy_score for q in qs_list if q.low_accuracy_score is not None]

        avg_high_score = round(sum(high_accuracy_scores) / len(high_accuracy_scores), 2) if high_accuracy_scores else None
        avg_low_score = round(sum(low_accuracy_scores) / len(low_accuracy_scores), 2) if low_accuracy_scores else None

        summary.append({
            'symbol': symbol,
            'total_predictions': total,
            'high_met_percentage': round((high_met / total) * 100, 1),
            'low_met_percentage': round((low_met / total) * 100, 1),
            'avg_high_accuracy_score': avg_high_score,
            'avg_low_accuracy_score': avg_low_score,
        })
    print(f"[Summary] Generated accuracy summary for {len(summary)} symbols")
    # Return the summary as a paginated response
    print(f"[Summary] Summary data: {summary}")

    return Response({"summary": summary})

