from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    path('', include('apps.core.urls')),
    path('', include('apps.users.urls')),
    path('partner/',include('apps.partners.urls')),
    path('advertiser/',include('apps.advertisers.urls')),
    path('manager/',include('apps.managers.urls')),
    path('api/', include('apps.tracking.urls')),
]
