from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('songview', views.songview, name='songview'),
]
