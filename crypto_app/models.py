from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Crypto(models.Model):

    time_create = models.DateTimeField(auto_now_add=False)
    cp_curr = models.CharField(max_length=255)
    curr = models.CharField(max_length=255)
    price = models.FloatField()


class Comment(models.Model):

    cat = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

