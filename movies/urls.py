from django.urls import path
from . import views


urlpatterns = [
    path('', views.movies),
    path('<int:movie_id>/', views.detail),
    path('<int:movie_id>/review/', views.review),
    path('search/', views.search),
    path("genres/", views.genres),
    path('get_movies/', views.get_movies),
    # path('random_movies/', views.random_movies),
    path('likemovie/<int:movie_id>/', views.like_movie),
    path('<int:movie_id>/review/<int:review_id>/', views.review_detail),
    path('recommend_movieList/',views.recommend_MovieList),
    path('recommend_movieListall/',views.recommend_MovieListall),
    path('movieList_for_game/',views.moviesForGame),
    path('<int:genre_id>/genre/',views.genreName),
    path('<int:person_id>/person/',views.personData)
    # genre_id 여러개는 어떻게 받지
]
