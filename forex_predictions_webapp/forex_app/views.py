from django.shortcuts import render

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
    predictions = Prediction.objects.filter(symbol=symbol).order_by('-forecast_time')[:50]
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

