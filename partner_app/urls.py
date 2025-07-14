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
    # Добавить редактирование платформы
    path('connect_project/<int:project_id>',views.connect_project,name="connect_project"),
    path('stop_partnership/<int:project_id>',views.stop_partnership,name="stop_partnership"),
    path('suspend_partnership/<int:project_id>',views.suspend_partnership,name='suspend_partnership'),
    
    # Рекламодатель
    path('add_project',views.add_project,name='add_project'),
    path('del_project/<int:project_id>',views.delete_project,name='del_project'),
    path('edit_project/<int:project_id>',views.edit_project,name='edit_project'),
    
    # Модератор
    ## Действия с платформами партнёров
    path('approve_platform/<int:platform_id>',views.approve_platform,name='approve_platform'),
    path('reject_platform/<int:platform_id>',views.reject_platform,name='reject_platform'),

    ## Действия с проектами рекламодателей
    path('approve_project/<int:project_id>',views.approve_project,name='approve_project'),
    path('reject_project/<int:project_id>',views.reject_project,name='reject_project'),

    # Просмотр информации о пользователях
    path('partner/<int:partner_id>', views.partner_detail, name='partner'),
    path('advertiser/<int:advertiser_id>',views.advertiser_detail, name='advertiser')
]