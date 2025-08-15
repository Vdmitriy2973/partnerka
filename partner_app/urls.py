from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('update_api_settings',views.update_api_settings,name='update_api_settings'),
    path('update_notifications_settings', views.update_notifications_settings, name='update_notifications_settings'),

    # Партнёр
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
    
    # Рекламодатель
    path('add_project',views.add_project,name='add_project'),
    path('del_project/<int:project_id>',views.delete_project,name='del_project'),
    path('edit_project/<int:project_id>',views.edit_project,name='edit_project'),
    path('stop_partnership_with_partner/<int:partner_id>',views.stop_partnership_with_partner,name="stop_partnership_with_partner"),
    
    # Модератор
    ## Действия с платформами партнёров
    path('approve_platform/<int:platform_id>',views.approve_platform,name='approve_platform'),
    path('reject_platform/<int:platform_id>',views.reject_platform,name='reject_platform'),

    ## Действия с проектами рекламодателей
    path('approve_project/<int:project_id>',views.approve_project,name='approve_project'),
    path('reject_project/<int:project_id>',views.reject_project,name='reject_project'),

    ## Действия с транзакциями партнёров
    path('approve_transaction/<int:transaction_id>/<int:partner_id>',views.approve_transaction,name='approve_transaction'),
    path('reject_transaction/<int:transaction_id>/<int:partner_id>',views.reject_transaction,name='reject_transaction'),

    # Просмотр информации о пользователях
    path('partner/<int:partner_id>', views.partner_detail, name='partner'),
    path('advertiser/<int:advertiser_id>',views.advertiser_detail, name='advertiser'),
    
    # Просмотр информации о площадках/проектах
    path('project/<int:project_id>',views.project_detail,name='project'),
    
    # Просмотр информации о площадках/проектах
    path('api/docs',views.api_docs,name='api_docs'),
    
    # Редирект партнёрской ссылки
    path("api/test",views.ProtectedAPIView.as_view(),name="api_test"),
    path("api/conversions", views.ConversionAPIView.as_view(), name="api_conversion"),
    path("api/clicks",views.ClickAPIView.as_view(),name="api_click"),

    path("block_user/<int:user_id>",views.block_user,name='block_user'),
    path("unblock_user/<int:user_id>",views.unblock_user,name='unblock_user')

]