from rest_framework import serializers
from .models import Movie, Review,Person,Genre
from django.contrib.auth import get_user_model
class MovieListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
  class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
      model = Review
      fields = ('content', 'rank', 'user', 'like_users', 'updated_at')
  reviews = ReviewListSerializer(read_only=True, many=True)
  class Meta:
    model = Movie
    fields = '__all__'

class ReviewListSerializer(serializers.ModelSerializer):
  class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
  user = UserSerializer(read_only=True)  # UserSerializer 사용

  class Meta:
      model = Review
      fields = '__all__'

    
class ReviewSerializer(serializers.ModelSerializer):
  class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = get_user_model()
      fields = '__all__'
  user = UserSerializer(read_only=True)  # UserSerializer 사용
  class Meta:
    model = Review
    fields = '__all__'
    read_only_fields = ('like_users', 'updated_at','created_at','movie')  # 읽기 전용 필드 추가

class GenreListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'
