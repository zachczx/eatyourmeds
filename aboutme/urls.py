from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('retro.html', views.retro, name='retro'),
]
