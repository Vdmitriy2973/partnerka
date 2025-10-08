from django.contrib import admin
from apps.managers.models import ManagerProfile

@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)