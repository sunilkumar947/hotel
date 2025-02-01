from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .models import BookingRoom, HotelRoomType, Rooms
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from .models import BookingRoom, Rooms
from datetime import datetime 



@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Rooms
    template_name = "home.html"
    context_object_name = "rooms"
    
    def get_queryset(self):
        rooms = Rooms.objects.all()
        print(rooms) 
        queryset = super().get_queryset()
        room_type = self.request.GET.get("room_type")
          # Get filter from query params
        if room_type:
            queryset = queryset.filter(room_type__room_type=room_type)
            print(queryset)  # Assuming room_type has a name field
        return queryset
        
    

class BookingRoomView(FormView):
   
    success_url = reverse_lazy("booking-confirmation")  # Redirect after successful booking

    

    def post(self, request, *args, **kwargs):
        """Handle form submission and save booking data."""

        room_type = request.POST.get("property_type")
        print(room_type,'rrrrrrrrrrrrrrrrrrrrrrrrr')
        check_in_date = request.POST.get("check_in_date")
        check_out_date = request.POST.get("check_out_date")
        check_in_time = request.POST.get("check_in_time")
        print(check_in_time)
        check_out_time = request.POST.get("check_out_time")
        guests = int(request.POST.get("guests"))
        rooms = int(request.POST.get("rooms"))
        total_cost = request.POST.get("total_cost")

        try:
            room = Rooms.objects.get(property_type=room_type)
            booking = BookingRoom(
                user=request.user if request.user.is_authenticated else None,
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                check_in_time=check_in_time,
                check_out_time=check_out_time,
                guests=guests,
                rooms=rooms,
                total_cost=total_cost
                
            )
            booking.save()
            return redirect(self.success_url)
        except Rooms.DoesNotExist:
            return HttpResponse("Invalid room selection", status=400)  # Handle invalid room selection




class BookingConfirmationView(LoginRequiredMixin, TemplateView):
    """Displays the booking confirmation page after a successful booking."""
    template_name = "booking_confirmation.html"

    def get_context_data(self, **kwargs):
        """Pass any required context data to the template."""
        context = super().get_context_data(**kwargs)
        context["message"] = "Your booking has been successfully confirmed!"
        return context