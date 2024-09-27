from django.urls import path
from app.password_service.views import (
    PasswordAPIView,
    PasswordSearchAPIView,
)

urlpatterns = [
    path('password/<str:service_name>', PasswordAPIView.as_view(), name='password_detail'),
    path('password/', PasswordSearchAPIView.as_view(), name='search_password'),
]

