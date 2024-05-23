from rest_framework import serializers
from movies.models import Genre
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import update_session_auth_hash, get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20)
    like_genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, required=False)

    def custom_signup(self, request, user):
        user.nickname = self.validated_data.get('nickname', '')
        user.save(update_fields=['nickname'])
        like_genres = self.validated_data.get('like_genre', [])
        for genre in like_genres:
            user.like_genre.add(genre)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['like_genre'] = self.validated_data.get('like_genre', [])
        return data_dict


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['nickname', 'followings', 'like_movie', 'like_genre']

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.followings.set(validated_data.get('followings', instance.followings.all()))
        instance.like_movie.set(validated_data.get('like_movie', instance.like_movie.all()))
        instance.like_genre.set(validated_data.get('like_genre', instance.like_genre.all()))
        instance.save()
        return instance
