import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import datetime

class CustomUserManager(BaseUserManager):
    """Manager for custom user model to handle email or username login."""
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('front-desk', 'Front Desk'),
        ('guest', 'Guest'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    # Add additional fields if needed, like phone number
    phone = models.CharField(max_length=15, blank=True, null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class ProfileSetup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.FileField(upload_to='adminProfilepic')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True)
    
    
    def __str__(self):
        return self.first_name
    

class HotelRoomType(models.Model):
    
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room_type = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_type.capitalize()
    
    

class Rooms(models.Model):
    GST_CHOICES = [
        (12, '12%'),
        (18, '18%'),
    ]

    room_type = models.ForeignKey(HotelRoomType, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=200, null=True, blank=True)
    room_img = models.ImageField(upload_to='rooms')
    room_rate = models.BigIntegerField()
    group_rate = models.BigIntegerField()
    clining_fees = models.BigIntegerField(null=True,default=0)
    room_service_fee = models.BigIntegerField(null=True,default=0)
    hrs_rate = models.FloatField()
    gst = models.IntegerField(choices=GST_CHOICES, default=12)  # GST field added

    def __str__(self):
        return self.property_type



