from django.contrib import admin
from apps.tracking.models import ClickEvent

@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ('partner_link', 'ip_address', 'user_agent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('partner_link__partner__user__email', 'ip_address')