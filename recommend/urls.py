from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index ),
    path('songs/', views.songs, name="songs"),
    path('home/', views.home, name="home"),
    path('home/new', views.newsongs, name="newhome"),
    path('addsong/', views.addsong, name="addsong"),
    path('removesong/', views.removesong, name="removesong"),
    path('songview/<int:songnumber>/', views.songview, name='songview'),
    path('rate/', views.rate, name="rate"),
    path('signup/', views.signup.as_view(), name='signup'),
    path('api/song/', views.SongListCreate.as_view() ),
    path('homepage/', views.homepage, name='homepage'),
    path('accounts/login/', views.login, name='login'),
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
