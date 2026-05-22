import requests
import pytest
import os
TOKEN = None
from tests.conftest import BASE_URL

@pytest.mark.order(9)
def test_admin_users_list(admin_login_data):
    global TOKEN
    TOKEN = admin_login_data
    respo = requests.get(f'{BASE_URL}/users/',headers={"Authorization": f"Bearer {TOKEN}"})
    assert respo.status_code == 200


@pytest.mark.order(10)
def test_admin_change_role(admin_login_data):
    global TOKEN
    TOKEN = admin_login_data
    response = requests.put(f'{BASE_URL}/users/1/role/',json={"role_name": "admin"},headers={"Authorization": f"Bearer {TOKEN}"})
    assert response.status_code == 200
    assert {'success':'role updated'} == response.json()