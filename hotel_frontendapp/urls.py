from django.contrib import admin
from django.urls import path, include
from .views import HomeView,BookingRoomView,BookingConfirmationView
# from .views import select_identity, upload_front, upload_back, upload_user_photo, complete_kyc, kyc_completed

urlpatterns = [
  
    path('home', HomeView.as_view(), name='home'),
    path('confirm-booking/', BookingRoomView.as_view(), name='confirm_booking'),
    path("booking-confirmation/", BookingConfirmationView.as_view(), name="booking-confirmation"),

    # path('select-identity/', select_identity, name="select_identity"),
    # path('upload-front/', upload_front, name="upload_front"),
    # path('upload-back/', upload_back, name="upload_back"),
    # path('upload-user-photo/', upload_user_photo, name="upload_user_photo"),
    # path('complete-kyc/', complete_kyc, name="complete_kyc"),
    # path('kyc-completed/', kyc_completed, name="kyc_completed"),

]
