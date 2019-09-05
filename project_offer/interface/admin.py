from django.contrib import admin
from interface.models import UserProfileInfo,Categories,Offer_discription,ShopProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Categories)
admin.site.register(Offer_discription)
admin.site.register(ShopProfile)