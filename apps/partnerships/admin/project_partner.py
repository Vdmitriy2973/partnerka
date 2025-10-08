from django.contrib import admin
from apps.partnerships.models import ProjectPartner

@admin.register(ProjectPartner)
class ProjectPartnerAdmin(admin.ModelAdmin):
    list_display = ('project', 'partner', 'status', 'joined_at')
    list_filter = ('status', 'joined_at')
    search_fields = ('project__name', 'partner__user__email')