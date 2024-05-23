import numpy as np
import random
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404
from .models import Movie, Review, Genre, Person
from accounts.serializers import UserSerializer
from .serializers import MovieSerializer, MovieListSerializer, PersonSerializer
from .serializers import ReviewSerializer, ReviewListSerializer, GenreSerializer, GenreListSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(['GET'])
def movies(request):
  # 전체 영화 조회
#   요청을 보낸 사람의 access 토큰과 받은 서버에 로그인된 사람의 엑세스 토큰이 같으면 반환. 
  movies = get_list_or_404(Movie)
  serializer = MovieListSerializer(movies, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def moviesForGame(request):
    
  genre_ids = request.query_params.getlist('genre_id')
    
  if not genre_ids:
      return Response({'detail': '장르 ID가 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
  
  # genre_ids로 영화 필터링
  movies = Movie.objects.filter(genres__in=genre_ids).distinct()
  
  if not movies.exists():
      return Response({'detail': '제공된 장르에 해당하는 영화가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
  
  serializer = MovieListSerializer(movies, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)
    
  

@api_view(['GET'])
def detail(request, movie_id):
  # 단일 영화 조회
  movie = get_object_or_404(Movie, pk=movie_id)
  serializer = MovieSerializer(movie)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def personData(request, person_id):
  # 단일 영화 조회
  person = get_object_or_404(Person, pk=person_id)
  serializer = PersonSerializer(person)
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def genreName(request, genre_id):
  # 단일 영화 조회
  genre = get_object_or_404(Genre, pk=genre_id)
  serializer = GenreSerializer(genre)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def genres(request):
    genres = get_list_or_404(Genre)
    serializer = GenreListSerializer(genres, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def search(request):
    movie_title = request.GET.get('movie_title')
    print(movie_title)
    # 빈 칸이면
    if not movie_title:
        return Response({"error": "영화를 검색해주세요"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # 영화 검색 # 수정 글자들어간 영화 모두검색하기
        movies = get_list_or_404(Movie)
        search_movies = []
        for movie in movies:
           if movie_title in movie.title:
              search_movies.append(movie)
        print(search_movies)
        serializer = MovieListSerializer(search_movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
        return Response({"error": "영화가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
  
@api_view(['POST','PUT'])
def like_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    User = get_user_model()
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
      user.like_movie.add(movie)
      serializer = UserSerializer(user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
      like_movies = user.like_movie.all()
      if movie in like_movies:
          user.like_movie.remove(movie)
      else:
          user.like_movie.add(movie)
      serializer = UserSerializer(user)
      return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_movies(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True) 
    return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def random_movies(request):
#     movies = Movie.objects.all()
#     random_movies = random.sample(list(movies), 16)
#     serializer = MovieListSerializer(random_movies, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
# like_movies가 있으면 밑에 함수. 없으면 genre에서 랜덤으로 뽑기.
# 좋아하는 장르만 뽑는 함수도 따로
# 화면은 ..
@api_view(['GET', 'POST'])
def review(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)
  # 해당 전체 리뷰 조회
  if request.method == 'GET':
    reviews = Review.objects.filter(movie=movie)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  # 해당 영화의 리뷰 작성
  if request.method == 'POST':
    serializer = ReviewSerializer(data=request.data)
    print(request.user)
    if serializer.is_valid(raise_exception=True):
      serializer.save(movie=movie, user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST', 'PUT'])
def review_detail(request, movie_id, review_id):
  review = get_object_or_404(Review, pk=review_id)
  # 리뷰 삭제
  if request.method == 'POST':
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  # 리뷰 수정
  elif request.method == 'PUT':
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

# 코사인 유사도를 계산하는 함수
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)  # 벡터의 내적 계산
    norm_vec1 = np.linalg.norm(vec1)  # 첫 번째 벡터의 크기 계산
    norm_vec2 = np.linalg.norm(vec2)  # 두 번째 벡터의 크기 계산
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0  # 벡터 크기가 0이면 유사도는 0으로 설정
    return dot_product / (norm_vec1 * norm_vec2)  # 코사인 유사도 계산

# 영화 유사도 행렬을 생성하는 함수
def create_movie_similarity_matrix():
    all_genres = list(Genre.objects.all())  # 모든 장르를 리스트로 가져오기
    all_movies = list(Movie.objects.all())  # 모든 영화를 리스트로 가져오기
    all_directors = list(Person.objects.filter(directed_movies__isnull=False).distinct())  # 감독 목록 가져오기
    all_actors = list(Person.objects.filter(acted_movies__isnull=False).distinct())  # 배우 목록 가져오기
    
    movie_index = {movie.id: idx for idx, movie in enumerate(all_movies)}  # 영화 ID와 인덱스를 매핑
    movie_vectors = []

    for movie in all_movies:
        movie_genres = movie.genres.all()
        movie_directors = movie.crew.all() if movie.crew.exists() else []  # 감독 목록 가져오기 (없을 경우 빈 리스트)
        movie_actors = movie.cast.all() if movie.cast.exists() else []  # 배우 목록 가져오기 (없을 경우 빈 리스트)
        if movie.vote_average:
            normalized_vote_average = movie.vote_average / 10  # 평점 (0-1 범위로 정규화)
        else:
            normalized_vote_average = 0  # 평점이 없으면 0으로 설정
        movie_vector = np.array([
            1 if genre in movie_genres else 0 for genre in all_genres
        ] + [
            1 if director in movie_directors else 0 for director in all_directors
        ] + [
            1 if actor in movie_actors else 0 for actor in all_actors
        ] + [
            normalized_vote_average / 10  # 평점 (0-1 범위로 정규화)
        ])
        movie_vectors.append(movie_vector)

    movie_vectors = np.array(movie_vectors)
    similarity_matrix = np.zeros((len(all_movies), len(all_movies)))

    for i in range(len(all_movies)):
        for j in range(len(all_movies)):
            if i != j:
                similarity_matrix[i][j] = cosine_similarity(movie_vectors[i], movie_vectors[j])

    return similarity_matrix, movie_index


@api_view(['GET'])
def recommend_MovieListall(request):
   movies = get_list_or_404(Movie)
   random_movies = random.sample(list(movies), 10)
   serializer = MovieListSerializer(random_movies, many=True)
   return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def recommend_MovieList(request):
    user = request.user
    user_liked_movies = user.like_movie.all()
    user_liked_genres = user.like_genre.all()
    movies = Movie.objects.filter(genres__in=user_liked_genres)
    # user_liked_movies = (Movie.objects.all())[:3]

    # if movies.count() < 10:
    #     random_movies = movies
    # else:
    #     random_movies = random.sample(list(movies), 10)
    #     serializer = MovieListSerializer(random_movies, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    all_movies = Movie.objects.all()
    similarity_matrix, movie_index = create_movie_similarity_matrix()
    
    movie_scores = np.zeros(len(all_movies))

    for liked_movie in user_liked_movies:
        liked_movie_idx = movie_index[liked_movie.id]
        movie_scores += similarity_matrix[liked_movie_idx]

    recommended_indices = movie_scores.argsort()[-10:][::-1]
    recommended_movies = [all_movies[int(idx)] for idx in recommended_indices if all_movies[int(idx)] not in user_liked_movies]
    serializer = MovieListSerializer(recommended_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

    # recommended_movie_data = [
    #     {
    #         'title': movie.title,  # 영화 제목
    #         'release_date': movie.release_date,  # 개봉일
    #         'popularity': movie.popularity,  # 인기도
    #         'vote_count': movie.vote_count,  # 투표 수
    #         'vote_average': movie.vote_average,  # 평균 평점
    #         'overview': movie.overview,  # 영화 개요
    #         'poster_path': movie.poster_path,  # 포스터 경로
    #         'genres': [genre.id for genre in movie.genres.all()],  # 장르 ID 리스트
    #         'dongjin_point': getattr(movie, 'dongjin_point', 0),  # 동진 포인트 (기본 값 0)
    #         'cast': [{'name': actor.name, 'id': actor.id} for actor in movie.cast.all()[:5]],  # 출연 배우 (최대 5명)
    #         'crew': [{'name': director.name, 'id': director.id} for director in movie.crew.all()[:3]]  # 감독 (최대 3명)
    #     }
    #     for movie in recommended_movies  # 추천 영화 리스트
    # ]
    # print(recommended_movie_data)
    # return Response({'recommended_movies': recommended_movie_data})

    # elif request.method == 'PUT':
    #     user_liked_genres = user.like_genre.all()
    #     genre_chosen = random.choice(list(user_liked_genres))
    #     movies = Movie.objects.filter(genres=genre_chosen)
    #     if movies.count() < 16:
    #         random_movies = movies
    #     else:
    #         random_movies = random.sample(list(movies), 16)
    #     serializer = MovieListSerializer(random_movies, many=True)
    #     response_data = {
    #         'genre_chosen': {
    #             'id': genre_chosen.id,
    #             'name': genre_chosen.name
    #         },
    #         'movies': serializer.data
    #     }

    #     return Response(response_data, status=status.HTTP_200_OK)
        # return Response(serializer.data, status=status.HTTP_200_OK)
