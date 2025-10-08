from django.contrib import admin
from apps.partners.models import PartnerActivity

@admin.register(PartnerActivity)
class PartnerActivityAdmin(admin.ModelAdmin):
    list_display = ('partner', 'activity_type', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('partner__user__email', 'ip_address')