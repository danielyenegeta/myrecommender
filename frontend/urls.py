from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('', views.index ),
    path('songs/', views.songs, name="songs"),
    path('home/', views.home, name="home"),
    path('home/new', views.newsongs, name="newhome"),
    path('addsong/', views.addsong, name="addsong"),
]
