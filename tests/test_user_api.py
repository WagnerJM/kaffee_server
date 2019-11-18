import pytest
import requests

register_user = {
        "username": "test",
        "password": "test2345",
        "email": "test@test.de"
    }

def test_register_user():
    r = requests.post("http://localhost:5001/api/v1/register", json=register_user)

    assert r.status_code == 201


def test_user_login():
    pass

def test_user_logout():
    pass
