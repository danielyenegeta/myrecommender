from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/song/', views.SongListCreate.as_view() ),
    path('songs/', views.songs, name='songs'),
    path('homepage/', views.homepage, name='homepage'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('addsong/', views.addsong, name='addsong'),
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
