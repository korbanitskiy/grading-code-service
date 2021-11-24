import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from users.crud import UserAlreadyExistsError
from users.main import app
from users.database import Base
from users.deps import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
client = TestClient(app)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db


def test_user_ping():
    response = client.get("/users/ping")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "pong"}


def test_user_add():
    response = client.post(
        "/users",
        json={
            'name': "TestUser",
            'email': "test_user@mail.com",
            'is_active': False,
        }
    )
    data = response.json()
    assert response.status_code == 201, response.text
    assert data['message'] == 'TestUser was added'


def test_duplicate_email_error():
    client.post(
        "/users",
        json={
            'name': "TestUser",
            'email': "test_user_error@mail.com",
            'is_active': False,
        }
    )

    with pytest.raises(UserAlreadyExistsError):
        client.post(
            "/users",
            json={
                'name': "Another User",
                'email': "test_user_error@mail.com",
                'is_active': True,
            }
        )
