from django.contrib import admin
from apps.advertisers.models import Project,ProjectParam

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'advertiser', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'advertiser__user__email')


admin.site.register(ProjectParam)