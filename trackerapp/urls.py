from django.urls import path
from . import views
from .views import EatLogin, EatLogout, EatRegister, EatList, EatDetails, EatCreate, EatUpdate, EatDelete
from .views import nextDose

app_name = 'eatyourmeds'
urlpatterns = [
    path('login/', EatLogin.as_view(), name='eatlogin'),
    path('logout/', EatLogout.as_view(), name='eatlogout'),
    path('register/', EatRegister.as_view(), name='eatregister'),
    path('', EatList.as_view(), name='eatlist'),
    path('med/<int:pk>/', EatDetails.as_view(), name='eatdetails'),
    path('create/', EatCreate.as_view(), name='eatcreate'),
    path('update/<int:pk>/', EatUpdate.as_view(), name='eatupdate'),
    path('update_complete/<int:pk>', EatUpdate.as_view(fields=['complete']), name='eatupdate_complete'),    
    path('delete/<int:pk>/', EatDelete.as_view(), name='eatdelete'),
    path('dose/<int:pk>/', views.nextDose, name='nextDose')
]
