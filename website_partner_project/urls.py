"""
URL configuration for website_partner_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.http import Http404
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required

# class CustomAdminSite(admin.AdminSite):
#     @method_decorator(login_required)
#     def admin_view(self, view, cacheable=False):
#         # Получаем стандартно обработанное view от родительского класса
#         admin_view = super().admin_view(view, cacheable)
        
#         # Создаем новую обертку с дополнительными проверками
#         def wrapped_view(request, *args, **kwargs):
#             if not (request.user.is_active and request.user.is_staff):
#                 raise Http404("Page not found")
#             return admin_view(request, *args, **kwargs)
            
#         return wrapped_view

#     def has_permission(self, request):
#         return (
#             request.user.is_active and 
#             request.user.is_authenticated and 
#             request.user.is_staff
#         )

# admin_site = CustomAdminSite(name='custom_admin')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('partner_app.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
