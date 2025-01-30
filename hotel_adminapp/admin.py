from django.contrib import admin
from  .models  import ProfileSetup,Rooms,HotelRoomType,User



# class AdminProfileSetup(admin.AdminSite):
#     disply_list = ('user', 'first_name', 'profile_picture', 'email')

admin.site.register(ProfileSetup)
admin.site.register(HotelRoomType)    
admin.site.register(Rooms) 

admin.site.register(User)