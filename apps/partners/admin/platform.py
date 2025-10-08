from django.contrib import admin
from apps.partners.models import Platform

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'partner__user__email')