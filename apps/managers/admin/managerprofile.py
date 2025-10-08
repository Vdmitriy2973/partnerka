from django.contrib import admin
from partner_app.models import ManagerProfile

@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)