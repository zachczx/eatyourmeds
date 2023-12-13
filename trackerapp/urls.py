from django.urls import path
from . import views
from .views import EatLogin, EatLogout, EatRegister, EatDetails, EatCreate, EatUpdate, EatDelete
from .views import newlist, DoseView, htmx_delete, htmx_create_dose, htmx_delete_dose, htmx_create_dose_auto
from .views import BetaCreateCourse, BetaCreateDose, BetaViewCourse

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
]

newversion = [
    path('view_course/<int:pk>/', BetaViewCourse.as_view(), name="betaviewcourse"),
    path('create_course/', BetaCreateCourse.as_view(), name="betacreatecourse"),
    path('create_dose/', BetaCreateDose.as_view(), name="betacreatedose"),
]

htmxpatterns = [
    path('view_course/<int:id>/add/', views.htmx_create_dose, name="htmx_create_dose"),
    path('view_course/<int:id>/addauto/', views.htmx_create_dose_auto, name="htmx_create_dose_auto"),
    path('dose/<int:id>/delete/', views.htmx_delete, name="htmx_delete"),
    path('view_course/<int:id>/delete/<int:doseid>', views.htmx_delete_dose, name="htmx_delete_dose"),
]

urlpatterns = urlpatterns + newversion + htmxpatterns