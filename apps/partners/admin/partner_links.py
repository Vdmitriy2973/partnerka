from django.contrib import admin

from apps.partners.models import PartnerLink


@admin.register(PartnerLink)
class PartnerLinkAdmin(admin.ModelAdmin):
    list_display = ('partner', 'project', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('partner__user__email', 'project__name')