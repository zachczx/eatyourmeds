from django.urls import path
from . import views
from .views import RankingList

urlpatterns = [
    path('', views.home, name='rankinghome'),
    path('list/<str:sessionid>/', RankingList.as_view(), name='rankinglist'),
    path('list/<str:sessionid>/add/', views.htmx_add_worker, name='htmx_add_worker'),
    path('rankingredirect', views.rankingredirect, name='rankingredirect'),
    path('new', views.new_session, name='new_session'),
    path('validate/htmx_validate_session/', views.htmx_validate_session, name='htmx_validate_session'),
    path('validate/htmx_existing_session/', views.htmx_existing_session, name='htmx_existing_session'),
    path('list/<str:sessionid>/delete/<int:workerid>', views.htmx_delete_worker, name='htmx_del_worker'),
    path('list/<str:sessionid>/save', views.htmx_save_sequence, name='htmx_save_sequence'),
    path('list/<str:sessionid>/savequota', views.htmx_save_quota, name='htmx_save_quota'),
]

