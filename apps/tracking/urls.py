from django.urls import path
from . import views

urlpatterns = [      
    path("conversions", views.ConversionAPIView.as_view(), name="api_conversion"),
    path("clicks",views.ClickAPIView.as_view(),name="api_click"),
]