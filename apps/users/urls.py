from django.urls import path

from .forms import HTMLPasswordResetForm
from . import views
urlpatterns = [
    # Главный обработчик личного кабинета
    path('dashboard',views.dashboard,name='dashboard'),
    
    # Auth
    path('auth/login',views.handle_login,name='login'),
    path('auth/register',views.handle_registration,name='register'),
    path('auth/logout', views.handle_logout, name='logout'),

    # Восстановление пароля
    path('password-recovery', 
         views.ProtectedPasswordResetView.as_view(
             template_name='recovery/reset_password.html',
             email_template_name='recovery/reset_password_email.html',
             subject_template_name='recovery/reset_password_subject.txt',
             form_class=HTMLPasswordResetForm
         ), 
         name='password_recovery'),
    
    path('password-recovery/done', 
         views.ProtectedPasswordResetDoneView.as_view(
             template_name='recovery/reset_password_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-recovery-confirm/<uidb64>/<token>', 
         views.ProtectedPasswordResetConfirmView.as_view(
             template_name='recovery/reset_password_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-recovery-complete', 
         views.ProtectedPasswordResetCompleteView.as_view(
             template_name='recovery/reset_password_complete.html'
         ), 
         name='password_reset_complete'),

    # Общие настройки пользователей
    path('settings/update_profile',views.update_profile,name='update_profile'),
    path('settings/update_password',views.update_password,name='update_password'),
    path('settings/update_email_notifications', views.update_email_notifications, name='update_email_notifications'),
]