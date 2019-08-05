from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from recommend.models import Song, CustomUser, Ratings, Scores
from recommend.views import matrix_factorization
from django.contrib.auth.decorators import login_required
from .forms import AddSongForm, RemoveSongForm
import numpy

# Create your views here.
def index(request):
    return render(request, 'frontend/index.html')

@login_required()
def songs(request):
	songlist = Song.objects.all().order_by('title')
	context = {'songs':songlist}
	return render(request, 'frontend/songs.html', context)

@login_required()
def home(request):
	if request.user.is_authenticated:
		songs = request.user.songs.all()
		ratings = Ratings.objects.filter(person=request.user).order_by('song_id')
		recommended = request.user.newsongs.all().order_by('title')
		context = {
		'songs':songs,
		'recoms':recommended,
		'ratings':ratings
		}
		return render(request, 'frontend/home.html', context)
	return render(request, 'frontend/home.html')

def newsongs(request):
	if request.user.is_authenticated:
		songs = request.user.songs.all()
		recommends = request.user.recommends.all()
		ratings = Ratings.objects.filter(person=request.user).order_by('song_id')
		num_songs = Song.objects.latest('id').id+1
		matrix = []

		allusers = CustomUser.objects.all().order_by('id')
		allsongs = Song.objects.all()
		for user in allusers:
			user_ratings = Ratings.objects.filter(person=user)
			to_append = []
			for i in range(1,num_songs):
				if user_ratings.filter(song_id=i).exists():
					to_append.append(user_ratings.get(song_id=i).rating)
				else:
					to_append.append(0)
			matrix.append(to_append)

		U = len(matrix)
		V = len(matrix[0])
		K = 7
		P = numpy.random.rand(U,K)
		Q = numpy.random.rand(V,K)
		nP, nQ = matrix_factorization(matrix, P, Q, K)
		nR = numpy.dot(nP, nQ.T)

		id = request.user.id
		for i in range(1, num_songs):
			in_songs = request.user.songs.filter(id=i).exists()
			in_newsongs = request.user.newsongs.filter(id=i).exists()
			if ratings.filter(song_id=i).exists():
				user_rating = ratings.get(song_id=i).rating
			else:
				user_rating = 0

			if in_newsongs:
				if (user_rating < 4 and user_rating > 0) or in_songs or nR[id-1][i-1] < 3:
					to_remove = request.user.newsongs.get(id=i)
					request.user.newsongs.remove(to_remove)
					continue
			elif not in_songs:
				if user_rating >= 4 or nR[id-1][i-1] >= 4:
					request.user.newsongs.add(allsongs.get(id=i))

		recommended = request.user.newsongs.all().order_by('title')


		context = {
		'songs':songs,
		'recoms':recommended,
		'ratings':ratings
		}
		return render(request, 'frontend/home.html', context)
	return render(request, 'frontend/home.html')

@login_required
def addsong(request):
    if request.method == "POST":
        form = AddSongForm(request.POST)
        if form.is_valid():
            song_title = form.cleaned_data['title']
            song_artist = form.cleaned_data['artist']
            song = Song.objects.get(title=song_title, artist=song_artist)
            request.user.songs.add(song)
            return redirect('/addsong')

    else:
        addform = AddSongForm()
        songs = Song.objects.all()
        context = {
        'addform':addform,
        'songs':songs
        }
        return render(request, 'frontend/addsong.html', context)

@login_required
def removesong(request):
    if request.method == "POST":
        form = RemoveSongForm(request.POST)
        if form.is_valid():
            song_title = form.cleaned_data['title']
            song_artist = form.cleaned_data['artist']
            song = Song.objects.get(title=song_title, artist=song_artist)
            request.user.songs.remove(song)
            return redirect('/removesong')

    else:
        removeform = RemoveSongForm()
        songs = Song.objects.all()
        context = {
        'removeform':removeform,
        'songs':songs
        }
        return render(request, 'frontend/removesong.html', context)
