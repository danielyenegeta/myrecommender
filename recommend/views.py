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
#
#
# songs = []
# songs.append('Power')
# songs.append('Magic')
# songs.append('Money Longer')
# songs.append('R.I.P.')
# songs.append('Claire de Lune')
#
# users = {}
# users['Future'] = {}
# users['Kanye'] = {}
# users['Jay Z'] = {}
# users['Steve Jobs'] = {}
# users['Bill Gates'] = {}
# users['Young Thug'] = {}
#
# users['Future'] = {
#         'Magic': 5,
#         'Money Longer': 3,
#         'R.I.P.': 4,
#         'Claire de Lune': 4.9
#     }
# users['Kanye'] = {
#         'Power': 5,
#         'Magic': 4.7,
#         'Money Longer': 1,
#         'R.I.P.': 5
#     }
# users['Jay Z'] = {
#         'Power': 4.1,
#         'Magic': 2.1,
#         'Money Longer': 4.7,
#         'Claire de Lune': 5
#     }
# users['Steve Jobs'] = {
#     'Power': 1.8,
#     'Magic': 4.6,
#     'R.I.P': 4.2,
#     'Claire de Lune': 5
#     }
# users['Bill Gates'] = {
#         'Magic': 2.1,
#         'Money Longer': 4.5,
#         'R.I.P.': 2,
#         'Claire de Lune': 5
#     }
# users['Young Thug'] = {
#         'Power': 2.3,
#         'Money Longer': 3.2,
#         'R.I.P.': 4.2
#     }
# songs.sort()
# matrix=[]
# for u in users:
#     ratings=[]
#     for v in songs:
#         if v in users[u]:
#             ratings.append(users[u][v])
#         else:
#             ratings.append(0)
#     matrix.append(ratings)
# matrix = numpy.array(matrix)
#
# U = len(matrix)
# V = len(matrix[0])
# K=10
# P = numpy.random.rand(U,K)
# Q = numpy.random.rand(V,K)
# nP, nQ = matrix_factorization(matrix, P, Q, K)
# nR = numpy.dot(nP, nQ.T)

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
			# if ratings.filter(song_id=i).exists():
			# 	if ratings.get(song_id=i).rating <= 2:
			# 		if in_newsongs:
			# 			to_remove = request.user.newsongs.get(id=i)
			# 			request.user.newsongs.remove(to_remove)
			# 		break
			# 	elif ratings.get(song_id=i).rating >= 4 and not in_newsongs:
			# 		request.user.newsongs.add(allsongs.get(id=i))
			# 		break
			# if nR[id_index][i-1] >= 4:
			# 	if not request.user.songs.filter(id=i).exists() and not in_newsongs:
			# 		request.user.newsongs.add(allsongs.get(id=i))
			# elif nR[id_index][i-1] < 3:
			# 	if in_newsongs:
			# 		to_remove = request.user.newsongs.get(id=i)
			# 		request.user.newsongs.remove(to_remove)
			in_songs = request.user.songs.filter(id=i).exists()
			in_newsongs = request.user.newsongs.filter(id=i).exists()
			if ratings.filter(song_id=i).exists():
				user_rating = ratings.get(song_id=i).rating

			if in_newsongs:
				if user_rating < 4 or in_songs or nR[id-1][i-1] < 3:
					to_remove = request.user.newsongs.get(id=i)
					request.user.newsongs.remove(to_remove)
					continue
			elif (user_rating >= 4 or nR[id-1][i-1] >= 4) and not in_songs:
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
