from django.contrib import admin
from django.urls import path, include
from .views import CalculateTotalCostView,HomeView,ConfirmBookingView

urlpatterns = [
  
    path('home', HomeView.as_view(), name='home'),
    path('calculate-total-cost/', CalculateTotalCostView.as_view(), name='calculate_total_cost'),
    path('confirm-booking/', ConfirmBookingView.as_view(), name='confirm_booking'),

]
