# Crypto REST_API
### REST_API information about currency and cryptocurrency rates

## Goals

Understand how to work with databases, requests, http protocol, multiprocessing in DRF (using celery and celery_beats),redis.
Also docker, dockerfile, docker-compose

## About

This program takes information from [site](https://ru.investing.com/crypto/bitcoin) via get requests, parses html from it and put into database.
After that you can in the browser take information from database(using get request). You can register and authorize
(using jwt token or session_id). After your authorization you can leave comments, update and delete it(using post, put and delete) and take the list of comments. 
Also you can get information about cryptocurrencies rates and average rates.
The project uses postgresql(port:5432), redis(port:6379). App runs using port:8000


In order to run it, you will need to download a list of Python modules(in requirement.txt). After that you should enter commands in the terminal:
1) docker-compose build
2) docker-compose up
