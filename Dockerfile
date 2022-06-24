FROM python:3.8

RUN apt-get update

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

#Декларируем порт, что бы потом его пробросить:
EXPOSE 8000

#Укажем переменную окружения:
ENV TZ Europe/Kiev

#Переменные окружения используются напр.:
# Указать путь к какому то файлу, ID-клиентов,
#URL

# Переменную окружения так же можно указать при сборке контейнера:
#docker run -p 8080:8080 -e TZ Europe/Kiev имя

CMD python3 manage.py makemigrations; python3 manage.py migrate; python3 manage.py runserver 0.0.0.0:8000



