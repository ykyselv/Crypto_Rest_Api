"""crypto_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, register_converter
from crypto_app.views import AverageAPIView, CryptoAPIView, CommentViewSet, UserAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers
from graphene_django.views import GraphQLView



admin.site.site_header = 'Crypto_app_administration'
admin.site.index_title = 'Our_admin_panel'

router = routers.SimpleRouter()
router.register(r'comment', CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/start/', CryptoAPIView.as_view(), name='list_rate'),
    path('api/start/average/', AverageAPIView.as_view(), name='average_rate'),
    path('api/userlist/', UserAPIView.as_view(), name='list_user'),
    path('api/jwt/create/', include('djoser.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # URL for comments:
    path('api/', include(router.urls), name='api_comment'),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]



