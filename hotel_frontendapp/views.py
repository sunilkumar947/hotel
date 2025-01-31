from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render
from .models import HotelRoomType, Rooms
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# 
@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Rooms
    template_name = "home.html"
    context_object_name = "rooms"

    def get_queryset(self):
        queryset = super().get_queryset()
        room_type = self.request.GET.get("room_type")
          # Get filter from query params
        if room_type:
            queryset = queryset.filter(room_type__room_type=room_type)
            print(queryset)  # Assuming room_type has a name field
        return queryset
        
    

    def post(self, request, *args, **kwargs):
        room_types = HotelRoomType.objects.all()
        room_type = request.POST.get('room_type')
        check_in_date_str = request.POST.get('check_in_date')
        check_out_date_str = request.POST.get('check_out_date')
        guests = int(request.POST.get('guests', 0))
        rooms = int(request.POST.get('rooms', 0))

        selected_room = Rooms.objects.filter(room_type__room_type=room_type).first()

        # Check if dates are provided
        if check_in_date_str and check_out_date_str:
            try:
                # Convert date strings into datetime objects
                check_in_date = datetime.strptime(check_in_date_str, "%Y-%m-%d")
                check_out_date = datetime.strptime(check_out_date_str, "%Y-%m-%d")
                
                # Calculate the number of days between check-in and check-out
                days = (check_out_date - check_in_date).days
            except ValueError:
                # If date parsing fails, handle the exception (e.g., invalid date format)
                days = 0
        else:
            days = 0

        if selected_room and days > 0:
            # Calculate the price and other fees
            room_rate = selected_room.room_rate
            cleaning_fees = selected_room.clining_fees
            room_service_fee = selected_room.room_service_fee

            # Calculate total room cost
            total_room_cost = room_rate * rooms * days
            total_before_taxes = total_room_cost + cleaning_fees + room_service_fee

            # Prepare context for rendering
            context = {
                'room_types': room_types,
                'selected_room': selected_room,
                'total_room_cost': total_room_cost,
                'total_before_taxes': total_before_taxes,
                'days': days
            }
        else:
            context = {'room_types': room_types}

        return render(request, 'home.html', context)





class CalculateTotalCostView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        
        room_id = data.get("room_id")
        check_in = datetime.strptime(data.get("check_in"), "%Y-%m-%d")
        check_out = datetime.strptime(data.get("check_out"), "%Y-%m-%d")
        rooms = int(data.get("rooms", 1))

        try:
            room = Rooms.objects.get(id=room_id)
            nights = (check_out - check_in).days or 1  # Ensure at least 1 night
            room_total = room.room_rate * nights * rooms
            cleaning_fee = room.clining_fees * rooms
            service_fee = room.room_service_fee * rooms
            tax_amount = (room_total + cleaning_fee + service_fee) * (room.gst / 100)
            final_total = room_total + cleaning_fee + service_fee + tax_amount

            return JsonResponse({
                "nights": nights,
                "room_rate": room.room_rate,
                "room_total": room_total,
                "cleaning_fee": cleaning_fee,
                "service_fee": service_fee,
                "taxes": round(tax_amount, 2),
                "final_total": round(final_total, 2)
            })
        except Rooms.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=400)

        return JsonResponse({"error": "Invalid request"}, status=400)


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import BookingRoom, Rooms
from hotel_adminapp.models import User

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import BookingRoom, Rooms
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BookingRoom, Rooms
from django.urls import reverse_lazy
from datetime import datetime

class ConfirmBookingView(LoginRequiredMixin, CreateView):
    model = BookingRoom
    fields = ['room', 'check_in_date', 'check_out_date', 'check_in_time', 'check_out_time', 'guests', 'rooms', 'total_cost']
    template_name = 'home.html'  # Replace with your actual template name

    def form_valid(self, form):
        # Get form data
        room = self.request.POST.get('room_type')

        check_in_date = self.request.POST.get('check_in_date')
        check_out_date = self.request.POST.get('check_out_date')

        check_in_hour = int(self.request.POST.get('check_in_hour'))
        check_in_minute = int(self.request.POST.get('check_in_minute'))
        check_in_period = self.request.POST.get('check_in_period')

        check_out_hour = int(self.request.POST.get('check_out_hour'))
        check_out_minute = int(self.request.POST.get('check_out_minute'))
        check_out_period = self.request.POST.get('check_out_period')

        guests = int(self.request.POST.get('guests'))
        rooms = int(self.request.POST.get('rooms'))
        total_cost = self.request.POST.get('total-cost')

        # Convert times to 24-hour format
        check_in_time = datetime.strptime(f"{check_in_hour}:{check_in_minute} {check_in_period}", "%I:%M %p").time()
        check_out_time = datetime.strptime(f"{check_out_hour}:{check_out_minute} {check_out_period}", "%I:%M %p").time()

        # Create and save the booking
        booking = form.save(commit=False)
        booking.user = self.request.user  # Associate with the logged-in user
        booking.room = room
        booking.check_in_date = check_in_date
        booking.check_out_date = check_out_date
        booking.check_in_time = check_in_time
        booking.check_out_time = check_out_time
        booking.guests = guests
        booking.rooms = rooms
        booking.total_cost = total_cost
        booking.save()

        return redirect('home')  # Redirect to a booking confirmation page (change URL name accordingly)

    def form_invalid(self, form):
        # Handle invalid form submission (if needed)
        return super().form_invalid(form)
