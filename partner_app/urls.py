from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    
    # Auth
    path('auth/login',views.handle_login,name='login'),
    path('auth/register',views.handle_registration,name='register'),
    path('auth/logout', views.handle_logout, name='logout'),
    
    
    # Главный обработчик личного кабинета
    path('dashboard',views.dashboard,name='dashboard'),
    
    # Обновить общие настройки у пользователей
    path('settings/update_profile',views.update_profile,name='update_profile'),
    path('settings/update_password',views.update_password,name='update_password'),
    path('settings/update_email_notifications', views.update_email_notifications, name='update_email_notifications'),
    
    # Партнёр
    # Функции партнёра
    path('partner/add_platform',views.add_platform,name='add_platform'),
    path('partner/del_platform/<int:platform_id>',views.delete_platform,name='del_platform'),
    path('partner/edit_platform/<int:platform_id>',views.edit_platform, name='edit_platform'),
    path('partner/connect_project/<int:project_id>',views.connect_project,name="connect_project"),
    path('partner/stop_partnership_with_project/<int:project_id>',views.stop_partnership_with_project,name="stop_partnership_with_project"),
    path('partner/suspend_partnership/<int:project_id>',views.suspend_partnership,name='suspend_partnership'),
    path('partner/resume_partnership/<int:project_id>',views.resume_partnership,name='resume_partnership'),
    path('partner/generate_partner_link/<int:partnership_id>',views.generate_link,name='generate_link'),
    path('partner/delete_partner_link/<int:link_id>',views.delete_partner_link,name='delete_partner_link'),
    path('partner/update_payout_settings',views.payout_settings_view,name='update_payout_settings'),
    path('partner/create_payout_request',views.create_payout_request,name='create_payout_request'),
    path('partner/read_notifications',views.read_partner_notifications,name='read_partner_notifications'),
    
    ## Страницы личного кабинета партнёра
    path('partner/dashboard',views.partner_dashboard,name='partner_dashboard'),
    path('partner/offers',views.partner_offers,name='partner_offers'),
    path('partner/connections',views.partner_connections,name='partner_connections'),
    path('partner/platforms',views.partner_platforms,name='partner_platforms'),
    path('partner/links',views.partner_links,name='partner_links'),
    path('partner/payments',views.partner_payments,name='partner_payments'),
    path('partner/settings',views.partner_settings,name='partner_settings'),
    path('partner/notifications',views.partner_notifications,name='partner_notifications'),
    path('partner/notifications/json',views.partner_notifications_json,name='partner_notifications_json'),
    path('partner/notifications/mark/<int:notification_id>', views.mark_notification_read, name='mark_notification_read'),
    path('partner/notifications/mark-all', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Рекламодатель
    # Функции рекламодателя
    path('advertiser/add_project',views.add_project,name='add_project'),
    path('advertiser/del_project/<int:project_id>',views.delete_project,name='del_project'),
    path('advertiser/edit_project/<int:project_id>',views.edit_project,name='edit_project'),
    path('advertiser/stop_partnership_with_partner/<int:partner_id>',views.stop_partnership_with_partner,name="stop_partnership_with_partner"),
    path('advertiser/top_up_balance',views.top_up_balance,name='top_up_balance'),
    path('advertiser/update_api_settings',views.update_api_settings,name='update_api_settings'),
    path('advertiser/update_requisites',views.update_requisites_settings,name='update_requisites_settings'),
    path('advertiser/read_notifications',views.read_advertiser_notifications,name='read_advertiser_notifications'),
    
    ## Страницы личного кабинета рекламодателя
    path('advertiser/dashboard',views.advertiser_dashboard,name='advertiser_dashboard'),
    path('advertiser/partners',views.advertiser_partners,name='advertiser_partners'),
    path('advertiser/sales',views.advertiser_sales,name='advertiser_sales'),
    path('advertiser/projects',views.advertiser_projects,name='advertiser_projects'),
    path('advertiser/settings',views.advertiser_settings,name='advertiser_settings'),
    path('advertiser/requisites',views.advertiser_requisites,name='advertiser_requisites'),
    
    # Модератор
    # Функции модератора
    path('manager/approve_platform/<int:platform_id>',views.approve_platform,name='approve_platform'),
    path('manager/reject_platform/<int:platform_id>',views.reject_platform,name='reject_platform'),
    path('manager/approve_project/<int:project_id>',views.approve_project,name='approve_project'),
    path('manager/reject_project/<int:project_id>',views.reject_project,name='reject_project'),
    path('manager/approve_transaction/<int:transaction_id>/<int:partner_id>',views.approve_transaction,name='approve_transaction'),
    path('manager/reject_transaction/<int:transaction_id>/<int:partner_id>',views.reject_transaction,name='reject_transaction'),
    path('manager/proccess_adv_transaction/<int:transaction_id>',views.proccess_adv_transaction,name='proccess_adv_transaction'),
    path('manager/approve_adv_transaction/<int:transaction_id>',views.approve_adv_transaction,name='approve_adv_transaction'),
    path('manager/reject_adv_transaction/<int:transaction_id>',views.reject_adv_transaction,name='reject_adv_transaction'),
    path("manager/block_user/<int:user_id>",views.block_user,name='block_user'),
    path("manager/unblock_user/<int:user_id>",views.unblock_user,name='unblock_user'),
    
    ## Страницы личного кабинета менеджера
    path('manager/dashboard',views.manager_dashboard,name='manager_dashboard'),
    path('manager/projects',views.manager_projects,name="manager_projects"),
    path('manager/platforms',views.manager_platforms,name="manager_platforms"),
    path('manager/users',views.manager_users,name="manager_users"),
    path('manager/partners',views.manager_partners,name="manager_partners"),
    path('manager/advertisers',views.manager_advertisers,name="manager_advertisers"),
    
    # Просмотр информации о пользователях
    path('partner/<int:partner_id>', views.partner_detail, name='partner'),
    path('advertiser/<int:advertiser_id>',views.advertiser_detail, name='advertiser'),
    path('advertiser_requisites/<int:advertiser_id>',views.advertiser_legal_details,name='advertiser_legal_details'),
    
    # Просмотр информации о проектах
    path('project/<int:project_id>',views.project_detail,name='project'),
    
    # Документация
    path('api/docs',views.api_docs,name='api_docs'),
    path('faq',views.faq,name='faq'),
    
    # REST API 
    path("api/conversions", views.ConversionAPIView.as_view(), name="api_conversion"),
    path("api/clicks",views.ClickAPIView.as_view(),name="api_click"),

    # SEO
    path("robots.txt",views.robots_txt,name="robots.txt")
    
    
]