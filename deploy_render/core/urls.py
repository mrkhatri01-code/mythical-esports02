from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('teams/', views.teams, name='teams'),
    path('players/', views.players, name='players'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('streams/', views.streams_list, name='streams'),
] 