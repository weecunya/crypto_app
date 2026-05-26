
from myproject.settings import BASE_URL


import pytest


#Поменяйте по необходимости, кроме этого файла значение переменной нигде не присваивается

BASE_URL = 'http://127.0.0.1:8000/api'


@pytest.fixture
def client_data_register():
    return {
        "email": "wica@dura.com",
        "password": "140509",
        "password2": "140509",
        "first_name": "wica",
        "last_name": "szmak",
    }


@pytest.fixture
def client_data_login():
    return  {
        "email": "wica@dura.com",
        "password": "140509"

 }


@pytest.fixture
def client_data_register_2():
    return {
        "email": "wica@example.com",
        "password": "140509",
        "password2": "140509",
        "first_name": "wica",
        "last_name": "szmak",
    }


@pytest.fixture
def client_data_login_2():
    return  {
        "email": "wica@example.com",
        "password": "140509"

 }
import requests

@pytest.fixture
def admin_login_data():
    params = {"email": "admin@example.com", "password": "admin123"}
    resp = requests.post(f'{BASE_URL}/login/', json=params)
    token = resp.json().get('access_token')
    return token

