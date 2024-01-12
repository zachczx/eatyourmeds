from django.urls import path
from . import views
from .views import RankingList

urlpatterns = [
    path('', views.home, name='rankinghome'),
    path('list/<str:id>/', RankingList.as_view(), name='rankinglist'),
    path('list/<str:id>/add/', views.htmx_add_worker, name='htmx_add_worker'),
    path('rankingredirect', views.rankingredirect, name='rankingredirect'),
    path('new', views.new_session, name='new_session'),
    path('validate/htmx_validate_session/', views.htmx_validate_session, name='htmx_validate_session'),
    path('validate/htmx_existing_session/', views.htmx_existing_session, name='htmx_existing_session'),
]

