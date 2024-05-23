from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre, Review

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True)
    lovepoint = models.IntegerField(default=0)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    like_movie = models.ManyToManyField(Movie, related_name='liked_users', blank=True)
    like_genre = models.ManyToManyField(Genre, blank=True)
