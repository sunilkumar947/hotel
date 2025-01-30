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

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Rooms, HotelRoomType,BookingRoom

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Rooms
    template_name = "home.html"
    context_object_name = "rooms"

    def get_queryset(self):
        queryset = super().get_queryset()
        room_type = self.request.GET.get("room_type")
        if room_type:
            queryset = queryset.filter(room_type__room_type=room_type)
        return queryset

    def post(self, request, *args, **kwargs):
        room_types = HotelRoomType.objects.all()
        room_type_name = request.POST.get('room_type')
        check_in_date_str = request.POST.get('check_in_date')
        check_out_date_str = request.POST.get('check_out_date')
        check_in_time_str = request.POST.get('check_in_time')
        check_out_time_str = request.POST.get('check_out_time')
        guests = int(request.POST.get('guests', 0))
        rooms = int(request.POST.get('rooms', 0))
        is_hourly = request.POST.get('is_hourly') == 'on'

        selected_room = Rooms.objects.filter(room_type__room_type=room_type_name).first()
        total_cost = 0

        if not selected_room:
            return render(request, 'home.html', {'room_types': room_types, 'error': 'Invalid room selection'})

        try:
            check_in_date = datetime.strptime(check_in_date_str, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out_date_str, "%Y-%m-%d").date()
            check_in_time = datetime.strptime(check_in_time_str, "%H:%M").time()
            check_out_time = datetime.strptime(check_out_time_str, "%H:%M").time()

            # Ensure valid date range
            if check_out_date < check_in_date or (check_out_date == check_in_date and check_out_time <= check_in_time):
                return render(request, 'home.html', {'room_types': room_types, 'error': 'Invalid check-in/check-out time'})

            # Calculate total cost
            if is_hourly:
                check_in = datetime.combine(check_in_date, check_in_time)
                check_out = datetime.combine(check_out_date, check_out_time)
                duration_in_hours = (check_out - check_in).total_seconds() / 3600
                if duration_in_hours <= 0:
                    duration_in_hours = 1  # Minimum 1-hour charge
                base_cost = rooms * selected_room.hrs_rate * duration_in_hours
            else:
                num_days = (check_out_date - check_in_date).days
                if num_days <= 0:
                    num_days = 1  # Minimum 1-day charge
                base_cost = rooms * selected_room.room_rate * num_days

            gst_rate = selected_room.gst / 100  # Convert percentage to decimal
            gst_amount = base_cost * gst_rate
            total_cost = base_cost + gst_amount

        except ValueError:
            return render(request, 'home.html', {'room_types': room_types, 'error': 'Invalid date/time format'})

        # Save booking
        booking = BookingRoom.objects.create(
            user=request.user,
            room=selected_room,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            check_in_time=check_in_time,
            check_out_time=check_out_time,
            guests=guests,
            rooms=rooms,
            is_hourly=is_hourly,
            total_cost=total_cost
        )

        context = {
            'room_types': room_types,
            'selected_room': selected_room,
            'total_cost': total_cost
        }

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



