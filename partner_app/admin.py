from django.contrib import admin

from .models import User, PartnerProfile, AdvertiserProfile, ManagerProfile,Platform,Project,ProjectPartner,Conversion,ClickEvent

admin.site.register(User)

@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id','traffic_source','balance')

@admin.register(AdvertiserProfile)
class AdvertiserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id','api_key','balance')

@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id']


admin.site.register(Platform)
admin.site.register(Project)
admin.site.register(ProjectPartner)
admin.site.register(Conversion)
admin.site.register(ClickEvent)