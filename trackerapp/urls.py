from django.urls import path
from . import views
from .views import EatLogin, EatLogout, EatRegister, EatDetails, EatCreate, EatUpdate, EatDelete
from .views import newlist, DoseView, htmx_delete 

urlpatterns = [
    path('login/', EatLogin.as_view(), name='eatlogin'),
    path('logout/', EatLogout.as_view(), name='eatlogout'),
    path('register/', EatRegister.as_view(), name='eatregister'),
    path('med/<int:pk>/', EatDetails.as_view(), name='eatdetails'),
    path('create/', EatCreate.as_view(), name='eatcreate'),
    path('update/<int:pk>/', EatUpdate.as_view(), name='eatupdate'),
    path('update_complete/<int:pk>', EatUpdate.as_view(fields=['complete']), name='eatupdate_complete'),    
    path('delete/<int:pk>/', EatDelete.as_view(), name='eatdelete'),
    path('dose/<int:pk>/', DoseView.as_view(), name='doseview'),
    path('', newlist.as_view(), name='newlist'),
    path('dose/<int:id>/delete/', views.htmx_delete, name="htmx_delete"),
]
