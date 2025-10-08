from django.urls import path
from . import views

urlpatterns = [
    # Функции
    path('add_project',views.add_project,name='add_project'),
    path('del_project/<int:project_id>',views.delete_project,name='del_project'),
    path('edit_project/<int:project_id>',views.edit_project,name='edit_project'),
    path('stop_partnership_with_partner/<int:partner_id>',views.stop_partnership_with_partner,name="stop_partnership_with_partner"),
    path('top_up_balance',views.top_up_balance,name='top_up_balance'),
    path('update_api_settings',views.update_api_settings,name='update_api_settings'),
    path('update_requisites',views.update_requisites_settings,name='update_requisites_settings'),
    path('read_notifications',views.read_advertiser_notifications,name='read_advertiser_notifications'),
    
    # ЛК
    path('dashboard',views.advertiser_dashboard,name='advertiser_dashboard'),
    path('partners',views.advertiser_partners,name='advertiser_partners'),
    path('sales',views.advertiser_sales,name='advertiser_sales'),
    path('projects',views.advertiser_projects,name='advertiser_projects'),
    path('settings',views.advertiser_settings,name='advertiser_settings'),
    path('requisites',views.advertiser_requisites,name='advertiser_requisites')
]