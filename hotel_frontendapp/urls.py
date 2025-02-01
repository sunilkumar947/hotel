from django.contrib import admin
from django.urls import path, include
from .views import HomeView,BookingRoomView,BookingConfirmationView

urlpatterns = [
  
    path('home', HomeView.as_view(), name='home'),
    
    path('confirm-booking/', BookingRoomView.as_view(), name='confirm_booking'),
    path("booking-confirmation/", BookingConfirmationView.as_view(), name="booking-confirmation"),

]
