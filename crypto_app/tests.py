import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Crypto, Comment
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import requests
import json

# создаёт несуществующий обьект, то есть имитирует обьект,
# Принцип работы: всё, что не относиться к самой функции(которую мы тестируем), можно подменить.
# При этом тестируемые функции не нужно адаптировать для тестов, mock сам подменяет обьекты в других модулях

import mock


class AveragerageTests(APITestCase):

    def setUp(self):
        now = datetime.now().isoformat(' ', 'minutes')
        dat = datetime.strptime(now, "%Y-%m-%d %H:%M")
        Crypto.objects.create(time_create=dat, cp_curr='BTC', curr='USD', price=0.89).save()
        Crypto.objects.create(time_create=dat, cp_curr='ETH', curr='UAH', price=94169.3).save()
        Crypto.objects.create(time_create=dat, cp_curr='ETH', curr='EUR', price=2676.29).save()


        user_1 = User.objects.create_user(username='Ivan', email='ivan96@gmail.com',password='Ivan*1953')
        user_1.save()

        user_2 = User.objects.create_user(username='Taras', email='taras2000@gmail.com', password='Ivan*1953')
        user_2.save()

        user_3 = User.objects.create_user(username='Olga', email='Olga25@gmail.com', password='Ivan*1953')
        user_3.save()

        self.user_1_token = Token.objects.create(user=user_1)
        self.user_2_token = Token.objects.create(user=user_2)
        self.user_3_token = Token.objects.create(user=user_3)

        # Comment.objects.create(id=1,title='Very good', content='Service works very good', cat_id=user_1.id)
        # Comment.objects.create(id=2,title='good', content='Service works good', cat_id=user_2.id)
        # Comment.objects.create(id=3,title='so-so', content='Service works so-so', cat_id=user_3.id)
        # Comment.objects.create(id=4,title='bad', content='Service works bad', cat_id=user_2.id)
        #

        # res = Comment.objects.filter(id=1)
        # if not res:
        self.comment1 = Comment.objects.create(title='Very good', content='Service works very good', cat_id=user_1.id)
        self.comment1.save()
        self.comment2 = Comment.objects.create(title='good', content='Service works good', cat_id=user_2.id)
        self.comment2.save()
        self.comment3 = Comment.objects.create(title='so-so', content='Service works so-so', cat_id=user_3.id)
        self.comment3.save()
        self.comment4 = Comment.objects.create(title='bad', content='Service works bad', cat_id=user_2.id)
        self.comment4.save()


    # ТАБЛИЦА ЮЗЕРОВ:
    # Тест на проверку юзеров:
    def test_user_list(self):
        response = self.client.get(reverse('list_user'))
        # print(response.json())
        # является ли статус ответа 200:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # # сколько юзеров у нас есть?
        self.assertEqual(len(response.data["results"]), 3)
        # Проверить вхождение данных в наш response:

        # TODO: Добавить всех юзеров
        self.assertTrue({'username':'Olga', 'email':'Olga25@gmail.com'} in response.json().get('results'))
        self.assertTrue({'username': 'Ivan', 'email': 'ivan96@gmail.com'} in response.json().get('results'))
        self.assertTrue({'username': 'Taras', 'email': 'taras2000@gmail.com'} in response.json().get('results'))


    def test_create_user(self):
        # print(reverse('create_user'))
        response = self.client.post('http://127.0.0.1:8000/api/jwt/create/users/', data={'username':'Andrey', 'email':'Andrey25@gmail.com',
                                                                                        'password':'Ivan*1953'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response1 = self.client.get(reverse('list_user'))
        self.assertEqual(len(response1.data["results"]), 4)

    # # ТАБЛИЦА КРИПТОВАЛЮТ:

    # Тест на проверку незалогиненым пользователем(пытаемся вытянуть среднее из таблицы Crypto)
    def test_rate_list_invalid(self):
        response = self.client.get(reverse('average_rate'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # # Тест на проверку залогиненым пользователем(пытаемся вытянуть среднее из таблицы Crypto)
    def test_rate_average(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.get(reverse('average_rate'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # # Тест на проверку залогиненым пользователем(пытаемся вытянуть среднее из таблицы Crypto с правильными параметрами)
    def test_rate_average_params(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {'crypt': 'BTC', 'curr': 'USD'}
        response = self.client.get(reverse('average_rate'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # # Тест на проверку залогиненым пользователем(пытаемся вытянуть среднее из таблицы Crypto с неправильными параметрами)
    def test_rate_average_params(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {'crypt': 'ETH', 'curr': 'UAH'}
        response = self.client.get(reverse('average_rate'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # # Тест на проверку незалогиненым пользователем(пытаемся вытянуть информацию о крипте из таблицы Crypto)
    def test_rate_list_invalid(self):
        response = self.client.get(reverse('list_rate'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # # Тест на проверку залогиненым пользователем(пытаемся вытянуть информацию о крипте из таблицы Crypto)
    def test_rate_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.get(reverse('list_rate'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # # # Тест на проверку залогиненым пользователем(пытаемся вытянуть информацию о крипте из таблицы Crypto, c правильными параметрами)
    def test_rate_list_params(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {'crypt': 'BTC', 'curr': 'USD'}
        response = self.client.get(reverse('list_rate'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data["results"]), 0)


    # # Тест на проверку залогиненым пользователем(пытаемся вытянуть информацию о крипте из таблицы Crypto, c неправильными параметрами)
    def test_rate_list_invalid_params(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {'crypt': 'BTC', 'curr': 'UAH'}
        response = self.client.get(reverse('list_rate'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)


    # ТАБЛИЦА КОММЕНТАРИЕВ:
    # # Поиск списка комментов(залогиненый юзер):
    def test_comment_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.get('http://127.0.0.1:8000/api/comment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertTrue({'id':self.comment1.id,'title':'Very good', 'content':'Service works very good', 'cat':self.comment1.cat_id} in response.json().get('results'))


    # # # поиск списка комментов(незалогиненый юзер):
    def test_comment_list_invalid(self):
        response = self.client.get('http://127.0.0.1:8000/api/comment/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    # # Тест на добавление нового коммента(незалогиненый юзер)
    def test_comment_add_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.post('http://127.0.0.1:8000/api/comment/',
                                    data={'title':'bad', 'content':'service works very bad'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Тест на добавление нового коммента(залогиненый юзер)
    def test_comment_add(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.post('http://127.0.0.1:8000/api/comment/',
                                    data={'title': 'bad', 'content': 'service works very bad'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data["results"]), 4)
        # проверим, есть ли в базе то, что мы добавили:
        response_g = self.client.get('http://127.0.0.1:8000/api/comment/')
        self.assertEqual(len(response_g.data["results"]), 5)


    # # Тест на обновление коммента(незалогиненый юзер):
    def test_comment_update_invalid(self):
        response = self.client.put('http://127.0.0.1:8000/api/comment/1/',
                                    data={'title': 'Wonderful', 'content': 'service works very wonderful', 'cat': 2})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # # Тест на обновление коммента(залогиненый юзер; обновляем коммент, который сами написали):
    def test_comment_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)
        response = self.client.put(f'http://127.0.0.1:8000/api/comment/{self.comment2.id}/',
                                    data={'title': 'Wonderful', 'content': 'service works very wonderful', 'cat': self.comment2.cat_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверим, есть ли в базе то, что мы добавили:
        response_g = self.client.get('http://127.0.0.1:8000/api/comment/')
        self.assertTrue({'id': self.comment2.id, 'title': 'Wonderful', 'content': 'service works very wonderful', 'cat': self.comment2.cat_id} in response_g.json().get('results'))



    # Тест на обновление коммента(залогиненый юзер; обновляем коммент, который написал другой юзер):
    def test_comment_update_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.put(f'http://127.0.0.1:8000/api/comment/{self.comment2.id}/',
                                   data={'title': 'Wonderful', 'content': 'service works very wonderful', 'cat': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверим, есть ли в базе то, что мы добавили:
        response_g = self.client.get('http://127.0.0.1:8000/api/comment/')
        self.assertFalse({'id': self.comment2.id, 'title': 'Wonderful', 'content': 'service works very wonderful', 'cat':  self.comment2.cat_id} in response_g.json().get('results'))


    # Тест на удаление коммента(незалогиненый юзер):
    def test_comment_delete_invalid(self):
        response = self.client.delete(f'http://127.0.0.1:8000/api/comment/{self.comment1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    # Тест на удаление коммента(залогиненый юзер; удаляем коммент, который сами написали):
    def test_comment_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)

        response = self.client.delete(f'http://127.0.0.1:8000/api/comment/{self.comment2.id}/')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверим, есть ли в базе то, что мы добавили:
        response_g = self.client.get('http://127.0.0.1:8000/api/comment/')
        # print(response_g.json())
        self.assertFalse({'id': self.comment2.id, 'title': 'Wonderful', 'content': 'service works very wonderful', 'cat': self.comment2.cat_id} in response_g.json().get('results'))




    # Тест на удаление коммента(залогиненый юзер; удаляем коммент, который создал другой юзер):
    def test_comment_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)

        response = self.client.delete(f'http://127.0.0.1:8000/api/comment/{self.comment3.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверим, есть ли в базе то, что мы добавили:
        response_g = self.client.get('http://127.0.0.1:8000/api/comment/')
        self.assertTrue({'id': self.comment3.id, 'title': 'so-so', 'content': 'Service works so-so', 'cat': self.comment3.cat_id} in response_g.json().get('results'))


