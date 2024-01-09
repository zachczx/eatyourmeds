from django.urls import path
from . import views
from .views import RankingList

urlpatterns = [
    path('', views.home, name='rankinghome'),
    path('list/<int:id>/', RankingList.as_view(), name='rankinglist')
]
