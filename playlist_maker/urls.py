from django.urls import path
from . import views
app_name = 'playlist_maker'


urlpatterns =[
    path('', views.index, name = 'index'),
    path('not_found/', views.artist_not_found, name = 'artist_not_found'),
    path('playlist/', views.show_playlist, name= 'show_playlist'),
]