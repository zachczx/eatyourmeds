from django.urls import path
from . import views
from .views import EatLogin, EatRegister, EatDetails, EatCreate
from .views import htmx_delete_course, htmx_create_dose, htmx_delete_dose, htmx_create_dose_auto, logout_view
from .views import BetaCreateCourse, BetaCreateDose, BetaViewCourse, BetaMain, BetaDeleteCourse, BetaUpdateCourse

urlpatterns = [
    path('login/', EatLogin.as_view(), name='eatlogin'),
    path('logout/', views.logout_view, name='eatlogout'),
    path('register/', EatRegister.as_view(), name='eatregister'),
    path('med/<int:pk>/', EatDetails.as_view(), name='eatdetails'),
    #path('create/', EatCreate.as_view(), name='eatcreate'),
    #path('update/<int:pk>/', EatUpdate.as_view(), name='eatupdate'),
    #path('update_complete/<int:pk>', EatUpdate.as_view(fields=['complete']), name='eatupdate_complete'),    
    #path('delete/<int:pk>/', EatDelete.as_view(), name='eatdelete'),
    #path('dose/<int:pk>/', DoseView.as_view(), name='doseview'),
    #path('', newlist.as_view(), name='newlist'),
]

newversion = [
    path('', BetaMain.as_view(), name='betamain'),
    path('course/<int:pk>/', BetaViewCourse.as_view(), name="betaviewcourse"),
    path('course/create/', BetaCreateCourse.as_view(), name="betacreatecourse"),
    path('course/dose/create/', BetaCreateDose.as_view(), name="betacreatedose"),
    path('course/<int:pk>/delete_p/', BetaDeleteCourse.as_view(), name="betadelete"),
    path('course/<int:pk>/update/', BetaUpdateCourse.as_view(), name='betaupdatecourse'),
]

htmxpatterns = [
    path('course/<int:id>/add/', views.htmx_create_dose, name="htmx_create_dose"),
    path('view_course/<int:id>/addauto/', views.htmx_create_dose_auto, name="htmx_create_dose_auto"),
    path('course/<int:id>/delete/', views.htmx_delete_course, name="htmx_delete_course"),
    path('course/view/<int:id>/delete/<int:doseid>/', views.htmx_delete_dose, name="htmx_delete_dose"),
]

urlpatterns = urlpatterns + newversion + htmxpatterns