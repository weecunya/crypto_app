import pytest



def test_register_positive(client):
    payload = {
        'username': "weecunya",
        'email':"wica@example.com",
        'first_name':"wica",
        'last_name': "szmak"
    }
    response = client.post("register/",data=payload)
    assert response.status_code == 200

def test_register_with_invalid_data(client):
    pass

def test_register_without_data(client):
    pass

def test_register_with_wrong_method(client):
    pass