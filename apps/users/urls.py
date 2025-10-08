from . import views
from django.urls import path


urlpatterns = [
    # Главный обработчик личного кабинета
    path('dashboard',views.dashboard,name='dashboard'),
    
    # Auth
    path('auth/login',views.handle_login,name='login'),
    path('auth/register',views.handle_registration,name='register'),
    path('auth/logout', views.handle_logout, name='logout'),

    # Общие настройки пользователей
    path('settings/update_profile',views.update_profile,name='update_profile'),
    path('settings/update_password',views.update_password,name='update_password'),
    path('settings/update_email_notifications', views.update_email_notifications, name='update_email_notifications'),
]