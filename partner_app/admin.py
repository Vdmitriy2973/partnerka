from django.contrib import admin

from partner_app.models import User, PartnerProfile, AdvertiserProfile, ManagerProfile,Platform,Project,ProjectPartner,Conversion,ClickEvent, PartnerActivity, AdvertiserActivity, PartnerTransaction,AdvertiserTransaction,AdvertiserRequisites,PartnerPayoutSettings


admin.site.register(User)

@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id','balance')

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
admin.site.register(PartnerActivity)
admin.site.register(AdvertiserActivity)
admin.site.register(PartnerTransaction)
admin.site.register(AdvertiserTransaction)
admin.site.register(AdvertiserRequisites)
admin.site.register(PartnerPayoutSettings)