from django.contrib import admin 

from apps.advertisers.models import AdvertiserRequisites

@admin.register(AdvertiserRequisites)
class AdvertiserRequisitesAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'responsible_person', 'inn', 'phone', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['organization_name', 'responsible_person', 'inn', 'ogrn']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'organization_name', 'responsible_person')
        }),
        ('Контактная информация', {
            'fields': ('legal_address', 'phone', 'email')
        }),
        ('Регистрационные данные', {
            'fields': ('ogrn', 'inn')
        }),
        ('Банковские реквизиты', {
            'fields': ('checking_account', 'correspondent_account', 'bik')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )