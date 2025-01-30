from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import update_last_login
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from .forms import RegistrationForm, LoginForm,ProfileSetupForm
from .models import User,ProfileSetup, Rooms
from django.contrib import messages


class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("login")  # Redirect to login after successful registration

    def form_valid(self, form):
        form.save()  # Save the user to the database
        return super().form_valid(form)

class LoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                update_last_login(None, user)  # Update the last login timestamp
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")  # Add this line
        return render(request, self.template_name, {"form": form})


# class HomeView(TemplateView):
#     template_name = "home.html"
   
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Logs out the user
        return redirect('login')


    
    
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # # Get basic statistics
        # context['total_bookings'] = Booking.objects.count()
        # context['total_users'] = User.objects.count()
        # context['total_rooms'] = Room.objects.count()
        # context['pending_bookings'] = Booking.objects.filter(status='Pending').count()

        # # Get recent bookings (limit to the last 5 for the dashboard)
        # context['recent_bookings'] = Booking.objects.order_by('-created_at')[:5]

        return context


class AdminSettings(TemplateView):
    template_name = "admin_settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_list'] = [
            {"name": "Profile Setting", "url": reverse("profile-setting")},
            {"name": "Hotel Setting", "url": reverse("hotel-setting")},
            {"name": "Event Setting", "url": reverse("event-setting")},
            {"name": "Subscriptions", "url": reverse("subscriptions")},
        ]
        return context


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ProfileSetupForm()
        return render(request, "profileSetup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ProfileSetupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success-page")  # Replace with your desired redirect
        return render(request, "profileSetup.html", {"form": form})





#------Get Room by service---------
class RoomListView(ListView):
    model = Rooms
    template_name = "rooms_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        queryset = super().get_queryset()
        room_type = self.request.GET.get("room_type")  # Get filter from query params
        if room_type:
            queryset = queryset.filter(room_type__room_type=room_type)  # Assuming room_type has a name field
        return queryset
    
    
    
    
      # Check user role and redirect accordingly
            #     if user.role == 'admin':
            #         return redirect("admin-dashboard")  # Replace with your admin dashboard URL name
            #     elif user.role == 'front-desk':
            #         return redirect("frontdesk-dashboard")  # Replace with your front desk dashboard URL name
            #     elif user.role == 'guest':
            #         return redirect("guest-dashboard")  # Replace with your guest dashboard URL name
            #     else:
            #         return redirect("dashboard")  # Default redirection if role doesn't match
            # else:
            #     form.add_error(None, "Invalid username or password")