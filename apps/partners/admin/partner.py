from django.contrib import admin
from apps.partners.models import PartnerProfile

@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance',)
    list_filter = ('user',)
    search_fields = ('user__email', 'user__first_name')