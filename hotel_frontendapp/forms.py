from django import forms
from .models import BookingRoom

class BookingRoomForm(forms.ModelForm):
    class Meta:
        model = BookingRoom
        fields = [
            "check_in_date", "check_out_date",
            "check_in_time", "check_out_time",
            "guests", "rooms", "is_hourly"
        ]
        widgets = {
            "check_in_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "check_out_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "check_in_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "check_out_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "guests": forms.NumberInput(attrs={"class": "form-control"}),
            "rooms": forms.NumberInput(attrs={"class": "form-control"}),
            "is_hourly": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
