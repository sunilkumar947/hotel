
from django.http import HttpResponse
from .models import BookingRoom, Rooms
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from .models import *
from hotel_adminapp.models import *
from hotel_adminapp.models import BookingDiscount
from django.contrib import messages


class HomeView(ListView):
    model = Rooms
    template_name = "home.html"
    context_object_name = "rooms"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("login")  # Redirect to login page
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        rooms = Rooms.objects.all()
        print(rooms) 
        queryset = super().get_queryset()
        room_type = self.request.GET.get("room_type")
        if room_type:
            queryset = queryset.filter(room_type__room_type=room_type)
            print(queryset) 
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discounts'] = self.room_discount()  
        return context
    
    def room_discount(self):
        return BookingDiscount.objects.all() or BookingDiscount.objects.none() 


class BookingRoomView(FormView):
    success_url = reverse_lazy("booking-confirmation")  # Redirect after successful booking
    def dispatch(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to access this page.")
                return redirect("login")  # Redirect to login page
            return super().dispatch(request, *args, **kwargs)
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
    
################ KYC #####################   

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import KYCDetails

# @login_required
# def select_identity(request):
#     if request.method == "POST":
#         identity_type = request.POST.get("identity_type")

#         if not identity_type:
#             return render(request, "select_identity.html", {"error": "Please select an identity type!"})

#         # Get or create a KYC record for the user
#         kyc, created = KYCDetails.objects.get_or_create(user=request.user)
#         kyc.identity_type = identity_type
#         kyc.save()

#         return redirect("upload_front")  # Move to the next step

#     return render(request, "select_identity.html")



# @login_required
# def upload_front(request):
#     if request.method == "POST":
#         front_image = request.FILES.get("front_image")
#         request.session["front_image"] = front_image.name
#         return redirect("upload_back")
#     return render(request, "upload_front.html")

# @login_required
# def upload_back(request):
#     if request.method == "POST":
#         back_image = request.FILES.get("back_image")
#         request.session["back_image"] = back_image
#         return redirect("upload_user_photo")
#     return render(request, "upload_back.html")


# @login_required
# def upload_user_photo(request):
#     if request.method == "POST":
#         user_photo = request.FILES.get("user_photo")
#         request.session["user_photo"] = user_photo.name
#         return redirect("complete_kyc")
#     return render(request, "upload_user_photo.html")

# @login_required
# def complete_kyc(request):
#     if request.method == "POST":
#         user = request.user
#         kyc_details, created = KYCDetails.objects.get_or_create(user=user)
#         kyc_details.identity_type = request.session.get("identity_type")
#         kyc_details.front_image = request.session.get("front_image")
#         kyc_details.back_image = request.session.get("back_image")
#         kyc_details.user_photo = request.session.get("user_photo")
#         kyc_details.is_verified = False
#         kyc_details.save()

#         return redirect("kyc_completed")

#     return render(request, "complete_kyc.html")

# @login_required
# def kyc_completed(request):
#     return render(request, "kyc_completed.html")

