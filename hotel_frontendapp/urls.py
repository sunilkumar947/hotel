from django.contrib import admin
from django.urls import path, include
from .views import CalculateTotalCostView,HomeView

urlpatterns = [
  
    path('', HomeView.as_view(), name='home'),
    path('calculate-total-cost/', CalculateTotalCostView.as_view(), name='calculate_total_cost'),

]
