import pytest
import requests
import os

from tests.conftest import BASE_URL


TOKEN = None


# Перед тестированием рекомендую очистить базу данных и загрузить пользователей из load_data

def test_register(client_data_register):
    response = requests.post(f'{BASE_URL}/register/', json=client_data_register)
    assert response.status_code == 201
    assert {'success':'user created'} == response.json()

def test_login(client_data_login):
    global TOKEN
    resp = requests.post(f'{BASE_URL}/login/', json=client_data_login)
    TOKEN = resp.json().get('access_token')
    assert resp.status_code == 200
    assert 'access_token' in resp.json().keys()


def test_profile():
    global TOKEN
    resp = requests.get(f'{BASE_URL}/profile/',headers={"Authorization": f"Bearer {TOKEN}"})
    assert resp.status_code == 200


def test_update_profile():
    global TOKEN
    resp = requests.put(f'{BASE_URL}/profile/update/',headers={"Authorization": f"Bearer {TOKEN}"},json={"first_name": "wicunya"})
    assert resp.status_code == 200
    assert resp.json() == {'success':'user updated'}


@pytest.mark.order(after="test_profile")
def test_delete_profile(client_data_register,client_data_login):
    global TOKEN
    resp = requests.delete(f'{BASE_URL}/profile/delete/',headers={"Authorization": f"Bearer {TOKEN}"})
    assert resp.status_code == 200
    assert resp.json() == {'success':'user deleted'}



