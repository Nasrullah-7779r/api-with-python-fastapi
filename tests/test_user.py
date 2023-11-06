import pytest
from fastapi import status
from app2 import schemas
from .test_db import client, session
import pdb

user_data_list = [
    {"name": "Adeel", "email": "adeel@example.com", "password": "123"},
    {"name": "Haider", "email": "haider@example.com", "password": "123"},
    {"name": "Ali", "email": "ali@example.com", "password": "123"}
]


# Base.metadata.create_all(bind=test_engine)  # responsible for execute initial configuration. etc tables creation


# @pytest.fixture
# def client():
#     # code before start test
#     Base.metadata.drop_all(bind=test_engine)
#     Base.metadata.create_all(bind=test_engine)  # responsible for execute initial configuration. etc tables creation
#     yield TestClient(app)
#     # code after finish test
#      # responsible for execute initial configuration. etc tables creation


@pytest.mark.parametrize("user_data", user_data_list)
def test_create_user(client, user_data):
    response = client.post('/create_user', json=user_data)
    new_user = schemas.UserOut(**response.json())
    expected_names = {"Adeel", "Haider", "Ali"}
    assert new_user.name in expected_names
    # print(new_user.email)
    assert response.status_code == status.HTTP_201_CREATED
    # pdb.set_trace()


def test_getall_user(client):
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


@pytest.mark.skip
def test_login(client):
    res = client.post("/login", data={"username": "haider@example.com", "password": "123"})
    print(res.json())
    assert res.status_code == status.HTTP_200_OK
