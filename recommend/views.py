from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Song, CustomUser, Ratings
from .forms import CustomUserCreationForm

# Create your views here.

class signup(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'

import numpy

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


			# else:
			# 	if user_rating >= 4 and not in_songs:
			# 		request.user.newsongs.add(allsongs.get(id=i))
			# 	elif nR[id-1][i-1] >= 4 and not in_songs:
			# 		request.user.newsongs.add(allsongs.get(id=i))


			# elif (user_rating >= 4 or nR[id-1][i-1] >= 4) and not in_songs:
			# 	request.user.newsongs.add(allsongs.get(id=i))
			# 	continue

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

def index(request):
    return render(request, 'recommend/index.html')

def songview(request):
	songs = Song.objects.all()
	context = {'song_list':songs}
	return render(request, 'recommend/home.html', context)

def mysongs(request):
	foo = CustomUser.objects.get(pk=1).recommends.all()
	context = {'user':foo}
	return render(request, 'recommend/songs.html', context)

def home(request, name):
	songs = Song.objects.order_by('title')
	context = {
	'song_list':songs,
	'user':name
	}
	return render(request, 'recommend/home.html', context)
