from requests import get, post, delete
from flask import request
from data.user_resources import UsersResource, UsersListResource

print(1, get('http://127.0.0.1:8080/api/v2/user').json())

print(2, get('http://127.0.0.1:8080/api/v2/user/1').json())

print(3, get('http://127.0.0.1:8080/api/v2/user/999').json())

print(4, post('http://127.0.0.1:8080/api/v2/user', json={}).json())

print(5, post('http://127.0.0.1:8080/api/v2/user', json={
    "surname": 'petrovich',
    "name": "oleg",
    'age': 31,
    "position": '13',
    "speciality": '13',
    "address": '13',
    'email': 'asdasdasd',
    "hashed_password": "31"}).json())

print(6, get('http://127.0.0.1:8080/api/v2/user/3').json())

print(7, delete('http://127.0.0.1:8080/api/v2/user/3').json())
