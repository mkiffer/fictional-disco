from django.urls import path
from . import views

urlpatterns = [
    path('auth/login', views.spotify_login, name='spotify-login'),
    path('auth/callback', views.spotify_callback, name='spotify-callback'),
    path('playlists', views.get_playlists, name='get-playlists'),
]
