from django.urls import path
from . import views

app_name = 'competitions'

urlpatterns = [
    path('', views.ChampionshipListView.as_view(), name='championship_list'),
    path('<int:pk>/', views.ChampionshipDetailView.as_view(), name='championship_detail'),
    path('create-season/', views.create_season_and_championships, name='create_season'),
]