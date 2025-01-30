from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ProfileSetup, Rooms

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "phone")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    
#Profile Setup Form
class ProfileSetupForm(forms.ModelForm):
        class Meta:
            model = ProfileSetup
            fields = [
                "profile_picture",
                "first_name",
                "last_name",
                "email",
                "mobile_number",
                "address",
                "zip_code",
                "country",
                "state",
                "city",
            ]
            widgets = {
                "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
                "first_name": forms.TextInput(attrs={"class": "form-control"}),
                "last_name": forms.TextInput(attrs={"class": "form-control"}),
                "email": forms.EmailInput(attrs={"class": "form-control"}),
                "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
                "address": forms.TextInput(attrs={"class": "form-control"}),
                "zip_code": forms.NumberInput(attrs={"class": "form-control"}),
                "country": forms.TextInput(attrs={"class": "form-control"}),
                "state": forms.TextInput(attrs={"class": "form-control"}),
                "city": forms.TextInput(attrs={"class": "form-control"}),
            }
