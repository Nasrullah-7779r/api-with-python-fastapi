import pytest
from fastapi import status
from jose import jwt
from app2 import schemas
from app2.config import setting
import pdb

user_data_list = [
    {"name": "Adeel", "email": "adeel@example.com", "password": "123"},
    {"name": "Haider", "email": "haider@example.com", "password": "123"},
    {"name": "Ali", "email": "ali@example.com", "password": "123"}
]


@pytest.mark.skip
@pytest.mark.parametrize("user_data", user_data_list)
def test_create_user(client, user_data):
    response = client.post('/create_user', json=user_data)
    new_user = schemas.UserOut(**response.json())
    expected_names = {"Adeel", "Haider", "Ali"}
    assert new_user.name in expected_names
    # print(new_user.email)
    assert response.status_code == status.HTTP_201_CREATED
    # pdb.set_trace()


@pytest.mark.skip
def test_get_all_user(client):
    response = client.get('/all_users')
    users_data = response.json()
    # pdb.set_trace()
    assert len(users_data) > 0
    user = users_data[0]
    assert user["name"] == "Adeel"
    user = users_data[1]
    assert user["name"] == "Haider"
    # print(user["email"])
    assert response.status_code == status.HTTP_200_OK


def test_login(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, setting.secret_key, setting.algorithm)
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK
