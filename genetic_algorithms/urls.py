from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('ejecutar-algoritmo/', views.ejecutar_algoritmo, name='ejecutar_algoritmo'),
]