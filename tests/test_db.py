import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app2.main import app
from fastapi.testclient import TestClient
from app2.DB import get_db, Base

SQLALCHEMY_TestDB_URL = 'postgresql://postgres:pass1234@localhost/FastAPI_testdb'

# SQLALCHEMY_DB_URL = (f'postgresql://{setting.database_username}:{setting.database_password}@'
#                      f'{setting.database_hostname}/{setting.database_name}')

test_engine = create_engine(SQLALCHEMY_TestDB_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="module")
def session():
    print("session is started")
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    print("client is started")

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
