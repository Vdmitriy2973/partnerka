from django.contrib import admin

from .models import User, AdvertiserProfile, PartnerProfile

admin.site.register(User)
admin.site.register(PartnerProfile)
admin.site.register(AdvertiserProfile)
