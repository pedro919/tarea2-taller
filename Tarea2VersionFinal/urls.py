"""Tarea2VersionFinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import artists_list, artists_detail, play_artist_tracks
from api.views import albums_list, albums_list_by_artist, albums_detail, play_album_tracks
from api.views import tracks_list, tracks_detail, tracks_list_by_album, tracks_list_by_artist, play_track

urlpatterns = [

    path('artists', artists_list, name='artists-list'),
    path('artists/<str:pk>', artists_detail, name='artists-detail'),
    path('artists/<str:pk>/albums/play', play_artist_tracks, name='play-artist-tracks'),


    path('albums', albums_list, name='albums-list'),
    path('artists/<str:pk>/albums', albums_list_by_artist, name='albums-by-artist'),
    path('albums/<str:pk>', albums_detail, name='albums-detail'),
    path('albums/<str:pk>/tracks/play', play_album_tracks, name='play-album-tracks'),

    path('tracks', tracks_list, name='tracks-list'),
    path('tracks/<str:pk>', tracks_detail, name='tracks-detail'),
    path('albums/<str:pk>/tracks', tracks_list_by_album, name='tracks-by-album'),
    path('artists/<str:pk>/tracks', tracks_list_by_artist, name='tracks-by-artist'),
    path('tracks/<str:pk>/play', play_track, name='play-track'),


]
