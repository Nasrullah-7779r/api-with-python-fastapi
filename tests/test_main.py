from fastapi.testclient import TestClient
from app2.main import app
from fastapi import status

client = TestClient(app)


def test_read_main():
    response = client.get('/')

    assert response.json().get("message") == "Hello FastAPI"
    print(response.json().get("message"))
    assert response.status_code == status.HTTP_200_OK
