from django.urls import path
from . import views

urlpatterns = [
    path('latest/', views.latest_predictions, name='latest_predictions'),
    path('predictions/<str:symbol>/', views.prediction_by_symbol, name='prediction_by_symbol'),
    path('predictions/', views.filtered_predictions, name='filtered_predictions'),  # For filters
    path('accuracy-summary/', views.accuracy_summary, name='accuracy_summary'), # New endpoint for accuracy summary
]
