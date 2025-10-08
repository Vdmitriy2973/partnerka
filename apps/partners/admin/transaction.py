from django.contrib import admin

from apps.partners.models import PartnerTransaction

@admin.register(PartnerTransaction)
class PartnerTransactionAdmin(admin.ModelAdmin):
    list_display = ('partner', 'amount', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('user__email',)