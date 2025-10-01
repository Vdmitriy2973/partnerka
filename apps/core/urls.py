from . import views
from django.urls import path


urlpatterns = [
    
    # Main pages
    path('',views.index,name='index'),
    path('feedback',views.feedback,name='feedback'),
    
    path('reviews',views.reviews,name='reviews'),
    path('make_review',views.make_review,name='make_review'),
    
    # Auth
    path('auth/login',views.handle_login,name='login'),
    path('auth/register',views.handle_registration,name='register'),
    path('auth/logout', views.handle_logout, name='logout'),
    
    # Документация
    path('api/docs',views.api_docs,name='api_docs'),
    path('faq',views.faq,name='faq'),
    
    # SEO
    path("robots.txt",views.robots_txt,name="robots.txt")   
]