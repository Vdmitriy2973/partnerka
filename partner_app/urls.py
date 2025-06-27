from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('add_platform',views.add_platform,name='add_platform'),
    path('del_platform/<int:platform_id>',views.delete_platform,name='del_platform'),
    path('project',views.project,name='project')
]