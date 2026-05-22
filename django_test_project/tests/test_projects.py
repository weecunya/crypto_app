import pytest
import requests
import os

TOKEN = None
from tests.conftest import BASE_URL

@pytest.fixture
def project_data():
    return {"name": "project_x", "status": "development"}


@pytest.mark.order(6)
def test_projects(admin_login_data):
    global TOKEN
    TOKEN = admin_login_data
    resp = requests.get(f'{BASE_URL}/projects/', headers={'Authorization': f"Bearer {TOKEN}"})
    assert resp.status_code == 200


@pytest.mark.order(7)
def test_create_project(project_data):
    global TOKEN
    resp = requests.post(f'{BASE_URL}/projects/create/', headers={'Authorization': f"Bearer {TOKEN}"},json = project_data)
    assert resp.status_code == 201
    assert {'success':'project created'} == resp.json()


@pytest.mark.order(after="test_create_project")
def test_delete_project():
    global TOKEN
    resp = requests.delete(f"{BASE_URL}/projects/3/delete/", headers={'Authorization': f"Bearer {TOKEN}"})
    assert resp.status_code == 200
    assert {'success':'project deleted'} == resp.json()

