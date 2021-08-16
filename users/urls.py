"""Definiuje wzorce adresóq URL dla aplikacji users."""

from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # Dołączenie domyślnych adresów URL uwierzytelnienia
    path('', include('django.contrib.auth.urls')),
    # Strona rejestracji
    path('register/', views.register, name='register'),
]