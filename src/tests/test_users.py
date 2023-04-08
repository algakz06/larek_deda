from fastapi.testclient import TestClient
import sys

print(sys.path)

from ..app.app import create_app


client = TestClient(create_app())


def test_creating_user():
    # valid user
    body = {
        "inn": 123215677652,
        "password": "SuperStr0ngPassw0rd",
        "usertype": 1,
    }
    response = client.post("/users/create", json=body)
    print(response.status_code, response.json())
    assert response.status_code == 200 or response.status_code == 403

    # invalid user

    body = {"inn": "testuser", "password": "SuperStr0ngPassw0rd", "usertype": 1}
    response = client.post("/users/create", data=body)

    assert response.status_code == 422


def test_auth():
    # valid credentials
    body = {
        "username": "123215677652",
        "password": "SuperStr0ngPassw0rd",
    }
    response = client.post("/auth/token", data=body)
    assert response.status_code == 200

    # invalid credentials
    body = {
        "username": "123215677652",
        "password": "SuperStr0ngPassw0rd1",
    }
    response = client.post("/auth/token", data=body)
    assert response.status_code == 401
    body = {
        "username": "p23215677652",
        "password": "SuperStr0ngPassw0rd",
    }
    response = client.post("/auth/token", data=body)
    assert response.status_code == 401
