from . import views
from django.urls import path


urlpatterns = [
    
    # Главная страница
    path('',views.index,name='index'),

    # Обратная связь
    path('feedback',views.feedback,name='feedback'),
    
    # Отзывы
    path('reviews',views.reviews,name='reviews'),
    path('make_review',views.make_review,name='make_review'),
    
    # Документация
    path('api/docs',views.api_docs,name='api_docs'),
    path('faq',views.faq,name='faq'),
    
    # Публичные страницы
    path('entities/partner/<int:partner_id>', views.partner_detail, name='partner'),
    path('entities/advertiser/<int:advertiser_id>',views.advertiser_detail, name='advertiser'),
    path('entities/project/<int:project_id>',views.project_detail,name='project'),
    path('entities/platform/<int:platform_id>',views.platform_detail,name='platform'),
    
    # SEO
    path("robots.txt",views.robots_txt,name="robots.txt")   
]