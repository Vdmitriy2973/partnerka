from django.contrib import admin

from .models import User, PartnerProfile, AdvertiserProfile, ManagerProfile,Platform,Project,ProjectPartner

admin.site.register(User)
admin.site.register(PartnerProfile)
admin.site.register(AdvertiserProfile)
admin.site.register(ManagerProfile)
admin.site.register(Platform)
admin.site.register(Project)
admin.site.register(ProjectPartner)