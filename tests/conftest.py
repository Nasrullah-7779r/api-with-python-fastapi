# it's a magic file. The user files of this file are able to access all the content without importing it
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app2.main import app
from fastapi.testclient import TestClient
from app2.DB import get_db, Base
from fastapi import status
from app2.oauth2 import create_access_token
from app2.models import Note
from app2.config import setting
import pdb


# SQLALCHEMY_DB_URL = (f'postgresql://{setting.database_username}:{setting.database_password}@'
#                      f'{setting.database_hostname}/{setting.database_name}')
SQLALCHEMY_TestDB_URL = (f'postgresql://{setting.database_username}:{setting.database_password}@'
                      f'{setting.database_hostname}/FastAPI_testdb')

test_engine = create_engine(SQLALCHEMY_TestDB_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Base.metadata.create_all(bind=test_engine)  # responsible for execute initial configuration. etc tables creation

@pytest.fixture
def session():
    print("session fixture started")
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    print("client is started")

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"name": "Haider", "email": "haider@example.com", "password": "123"}
    res = client.post("/create_user", json=user_data)
    print(res.json())
    assert res.status_code == status.HTTP_201_CREATED
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    token = create_access_token(data={"id": test_user["id"]})
    # pdb.set_trace()
    return token


@pytest.fixture
def authorized_client(token, client):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# @pytest.fixture
# def test_notes(authorized_client):
#     pdb.set_trace()
#     res = authorized_client.post("/create_note", json={"title": "test_note", "description": "test description"})
#     assert res.status_code == status.HTTP_201_CREATED


@pytest.fixture
def test_notes(test_user, session):
    note_data = [
        {
            "title": "Life",
            "description": "Life is unpredictable",
            "owner_id": test_user["id"]
        },
        {
            "title": "Understanding",
            "description": "Understanding is the core of learning",
            "owner_id": test_user["id"]
        },
        {
            "title": "Comparison",
            "description": "Comparison is the thief of Happiness",
            "owner_id": test_user["id"]
        },
    ]

    def create_note_model(note):
        return Note(**note)

    note_map = map(create_note_model, note_data)
    notes = list(note_map)
    session.add_all(notes)
    session.commit()
    notes = session.query(Note).all()
    return notes
