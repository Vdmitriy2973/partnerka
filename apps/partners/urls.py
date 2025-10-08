from django.urls import path
from . import views

urlpatterns = [    
    # Функции
    path('add_platform',views.add_platform,name='add_platform'),
    path('del_platform/<int:platform_id>',views.delete_platform,name='del_platform'),
    path('edit_platform/<int:platform_id>',views.edit_platform, name='edit_platform'),
    path('connect_project/<int:project_id>',views.connect_project,name="connect_project"),
    path('stop_partnership_with_project/<int:project_id>',views.stop_partnership_with_project,name="stop_partnership_with_project"),
    path('suspend_partnership/<int:project_id>',views.suspend_partnership,name='suspend_partnership'),
    path('resume_partnership/<int:project_id>',views.resume_partnership,name='resume_partnership'),
    path('generate_partner_link/<int:partnership_id>',views.generate_link,name='generate_link'),
    path('delete_partner_link/<int:link_id>',views.delete_partner_link,name='delete_partner_link'),
    path('update_payout_settings',views.payout_settings_view,name='update_payout_settings'),
    path('create_payout_request',views.create_payout_request,name='create_payout_request'),
    path('read_notifications',views.read_partner_notifications,name='read_partner_notifications'),
    
    # ЛК
    path('dashboard',views.partner_dashboard,name='partner_dashboard'),
    path('offers',views.partner_offers,name='partner_offers'),
    path('connections',views.partner_connections,name='partner_connections'),
    path('platforms',views.partner_platforms,name='partner_platforms'),
    path('links',views.partner_links,name='partner_links'),
    path('payments',views.partner_payments,name='partner_payments'),
    path('settings',views.partner_settings,name='partner_settings'),
    path('notifications',views.partner_notifications,name='partner_notifications'),
    path('notifications/json',views.partner_notifications_json,name='partner_notifications_json'),
    path('notifications/mark/<int:notification_id>', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all', views.mark_all_notifications_read, name='mark_all_notifications_read')
]