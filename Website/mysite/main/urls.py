"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('register/', views.register, name='register'),
    path("<int:id>", views.index, name="index"),
    path('players/', views.table_view, name='table_view'),
    path('edit/<int:pk>/', views.edit_view, name='edit_table'),
    path('delete_entry/<int:pk>/', views.delete_entry, name='delete_entry'),
]
"""
from django.urls import path
from . import views  # Import views from your main app

urlpatterns = [
    path("", views.home, name="home"),
    path('players/', views.players_list, name='players_list'),
    path('player/add/', views.player_add, name='player_add'),
    path('player/<int:player_id>/edit/', views.player_edit, name='player_edit'),
    path('player/<int:player_id>/delete/', views.player_delete, name='player_delete'),

    path('teams/', views.teams_list, name='teams_list'),
    path('team/add/', views.team_add, name='team_add'),
    path('team/<int:team_id>/edit/', views.team_edit, name='team_edit'),
    path('team/<int:team_id>/delete/', views.team_delete, name='team_delete'),

    path('stats/', views.stats, name="stats"),
]
