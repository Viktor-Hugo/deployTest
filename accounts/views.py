from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Movie, Review, User
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


@api_view(['GET', 'PUT', 'POST'])
def profile(request, username):
    user = get_object_or_404(User, username=username)


    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.user != user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        user.delete()
        return Response({"message": "회원 탈퇴가 성공적으로 처리되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def user_ranking(request):
    # 유저 모델 가져오기
    User = get_user_model()
    
    # lovepoint 순으로 유저 리스트 가져오기
    users_sorted_by_lovepoint = User.objects.all().order_by('-lovepoint')
    
    # 시리얼라이저를 사용하여 데이터 직렬화
    serializer = UserSerializer(users_sorted_by_lovepoint, many=True)
    
    # 직렬화된 데이터를 응답으로 반환
    return Response(serializer.data, status=status.HTTP_200_OK)

    
