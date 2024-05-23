"""
URL configuration for dongjin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views
from dj_rest_auth.registration.views import RegisterView
from accounts.serializers import UserRegisterSerializer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('movies.urls')),
    path('profile/<str:username>/', views.profile),
    path('user_ranking/',views.user_ranking),

    # dj-rest-auth
    path('accounts/', include('dj_rest_auth.urls')),
    # 'dj-rest-auth[with_social]'
    path('accounts/signup/', RegisterView.as_view(serializer_class=UserRegisterSerializer)),
]
