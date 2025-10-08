from django.contrib import admin 

from apps.advertisers.models import AdvertiserProfile

@admin.register(AdvertiserProfile)
class AdvertiserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_key', 'balance')
    list_filter = ('user',)
    search_fields = ('user__email',)