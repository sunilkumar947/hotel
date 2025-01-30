from django import views
from django.urls import path,include
from . views import *
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    # path("register/", RegisterView.as_view(), name="register"),
    # path("login/", LoginView.as_view(), name="login"),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("settings/", AdminSettings.as_view(), name="settings"),
    path('profile/', ProfileUpdateView.as_view(), name='profile-setting'),
    path('hotel/', AdminSettings.as_view(), name='hotel-setting'),
    path('event/', AdminSettings.as_view(), name='event-setting'),
    path('subscriptions/', AdminSettings.as_view(), name='subscriptions'),
    path('accounts/', include('allauth.urls')),  # Include Django AllAuth URLs
    
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    # path("home", HomeView.as_view(), name="home"),
    path('logout', LogoutView.as_view(), name='logout'),  # Add this line



]
