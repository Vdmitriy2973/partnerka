from django.contrib import admin
from apps.advertisers.models import AdvertiserTransaction

@admin.register(AdvertiserTransaction)
class AdvertiserTransactionAdmin(admin.ModelAdmin):
    list_display = ('advertiser', 'amount', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('advertiser__user__email',)