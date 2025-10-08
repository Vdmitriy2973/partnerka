from django.contrib import admin

from apps.advertisers.models import AdvertiserActivity

@admin.register(AdvertiserActivity)
class AdvertiserActivityAdmin(admin.ModelAdmin):
    list_display = ('advertiser', 'activity_type', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('advertiser__user__email', 'ip_address')