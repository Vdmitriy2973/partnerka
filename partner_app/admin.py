from django.contrib import admin

from .models import User, AdvertiserProfile, PartnerProfile,ManagerProfile, Platform

admin.site.register(User)
admin.site.register(PartnerProfile)
admin.site.register(AdvertiserProfile)
admin.site.register(ManagerProfile)
admin.site.register(Platform)