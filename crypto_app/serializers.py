from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Crypto, Comment


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
