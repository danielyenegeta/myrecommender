from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Song, CustomUser, Ratings, Scores
from .forms import CustomUserCreationForm, AddSongForm, RemoveSongForm, RateSongForm
from django.contrib.auth.decorators import login_required
from .serializers import SongSerializer
from rest_framework import generics
import numpy

# Create your views here.
class signup(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'

class SongListCreate(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

@login_required
def index(request):
    return render(request, 'frontend/index.html')

@login_required()
def songs(request):
	songlist = Song.objects.all().order_by('title')
	context = {'songs':songlist}
	return render(request, 'frontend/songs.html', context)

@login_required
def home(request):
	if request.user.is_authenticated:
		songs = request.user.songs.all()
		#last_practiced = request.user.songs.through.objects.filter(customuser_id=request.user.id)
		ratings = Ratings.objects.filter(person=request.user).order_by('song_id')
		recommended = request.user.newsongs.all().order_by('title')
		context = {
		'songs':songs,
		#'last_practiced':last_practiced,
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
        usersongs = request.user.newsongs.all().order_by('title')
        songs = Song.objects.all().order_by('title')
        context = {
        'addform':addform,
        'usersongs':usersongs,
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
        songs = request.user.songs.all().order_by('title')
        context = {
        'removeform':removeform,
        'songs':songs
        }
        return render(request, 'frontend/removesong.html', context)

@login_required
def rate(request):
    if request.method == "POST":
        form = RateSongForm(request.POST)
        if form.is_valid():
            ratings = Ratings.objects.filter(person=request.user)
            currsong = form.cleaned_data['song']
            currartist = form.cleaned_data['artist']
            currrating = form.cleaned_data['rating']
            toRate = Song.objects.get(title=currsong, artist=currartist)
            if ratings.filter(song_id=toRate.id).exists():
                toEdit = ratings.filter(song_id=toRate.id)
                if currrating == 0:
                    toEdit.delete()
                else:
                    toEdit.update(rating=currrating)
            elif currrating != 0:
                rate = Ratings.objects.create(person=request.user, song=toRate, rating=currrating)
            return redirect('/rate')
    else:
        form = RateSongForm()
        songs = Song.objects.all().order_by('title')
        context = {
        'form':form,
        'songs':songs
        }
        return render(request, 'frontend/rate.html', context)

@login_required
def songview(request, songnumber):
	if Scores.objects.filter(song_id=songnumber).exists():
		sheetmusic = Scores.objects.get(song_id=songnumber).pdf
		response = HttpResponse(sheetmusic.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'inline;filename=some_file.pdf'
		return response
		sheetmusic.close()
	else:
		return render(request, 'frontend/songview.html')


def matrix_factorization(R, P, Q, K, alpha=0.0002, beta=0.02, steps=10000):
	Q = Q.T
	for step in range(steps):
		for i in range(len(R)):
			for j in range(len(R[i])):
				if R[i][j] > 0:
					eij = R[i][j] - numpy.dot(P[i,:], Q[:, j])
					for k in range(K):
						P[i][k] = P[i][k] + alpha*(2*eij*Q[k][j]-beta*P[i][k])
						Q[k][j] = Q[k][j] + alpha*(2*eij*P[i][k]-beta*Q[k][j])
		eR = numpy.dot(P,Q)
		e = 0
		for i in range(len(R)):
			for j in range(len(R[i])):
				if R[i][j] > 0:
					e = e + pow(R[i][j] - numpy.dot(P[i,:], Q[:,j]), 2)
					for k in range(K):
						e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
		if e < 0.001:
			break
	return P, Q.T

@login_required
def homepage(request):
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
		'ratings':ratings,
		'matrix':matrix,
		'newmatrix':nR
		}
		return render(request, 'recommend/homepage.html', context)
	return render(request, 'recommend/homepage.html')

def login(request):
	return redirect('/login')