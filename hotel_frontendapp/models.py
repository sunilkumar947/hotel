from django.db import models
import datetime
from django.db import models
from datetime import datetime
from hotel_adminapp.models import User,Rooms,HotelRoomType






# Create your models here.
class BookingRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    guests = models.IntegerField()
    rooms = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    booking_date = models.DateTimeField(auto_now_add=True)
    is_hourly = models.BooleanField(default=False, help_text="Set to True for hourly bookings.")

    def save(self, *args, **kwargs):
        """Automatically calculate total cost including GST before saving the booking."""
        if self.check_in_date and self.check_out_date and self.room:
            base_cost = 0  # Initial cost before GST

            if self.is_hourly:
                # Calculate hourly cost
                check_in_time = datetime.combine(self.check_in_date, self.check_in_time)
                check_out_time = datetime.combine(self.check_out_date, self.check_out_time)
                duration_in_hours = (check_out_time - check_in_time).total_seconds() / 3600
                if duration_in_hours <= 0:
                    duration_in_hours = 1  # Minimum 1 hour charge
                base_cost = self.rooms * self.room.hrs_rate * duration_in_hours
            else:
                # Calculate daily cost
                num_days = (self.check_out_date - self.check_in_date).days
                if num_days <= 0:
                    num_days = 1  # Minimum 1 day charge
                base_cost = self.rooms * self.room.room_rate * num_days

            # Apply GST
            gst_rate = self.room.gst / 100  # Convert percentage to decimal
            gst_amount = base_cost * gst_rate

            # Final total cost including GST
            self.total_cost = base_cost + gst_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username if self.user else 'Guest'} for {self.rooms} room(s), Total Cost: {self.total_cost}"