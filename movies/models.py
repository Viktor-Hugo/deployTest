from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

class Person(models.Model):
    name = models.CharField(max_length=255)
    poster_path = models.URLField(blank=True, null=True)
    character = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    
class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(blank=True, null=True)  
    popularity = models.FloatField(blank=True, null=True)  # 비어있는 값을 허용
    vote_count = models.IntegerField(blank=True, null=True)  # 비어있는 값을 허용
    vote_average = models.FloatField(blank=True, null=True)  # 비어있는 값을 허용
    overview = models.TextField(blank=True, null=True)  # 비어있는 값을 허용
    poster_path = models.CharField(max_length=200, null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    dongjin_point = models.FloatField(default = 5)
    cast = models.ManyToManyField(Person, related_name='acted_movies',blank=True)
    crew = models.ManyToManyField(Person, related_name='directed_movies',blank=True)
    
def validate_rank(value):
    if not 1 <= value <= 10:
        raise ValidationError('1에서 10점 사이의 점수를 입력해주세요')
    
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rank = models.IntegerField(validators=[validate_rank])  
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
