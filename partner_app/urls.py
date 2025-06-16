from django.conf import settings
from django.urls import include, path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name='index')
]