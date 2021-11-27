import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from users.database import Base
from users.deps import get_db
from users.main import app
from users.models import User


@pytest.fixture(scope='session')
def client():
    return TestClient(app)


@pytest.fixture(scope='session', autouse=True)
def db():
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    def get_test_db():
        local_session = Session()
        try:
            yield local_session
        finally:
            local_session.close()

    app.dependency_overrides[get_db] = get_test_db

    yield session
    session.close()


@pytest.fixture()
def john(db):
    john = User(name='john', email='john@mail.com', is_active=True)
    db.add(john)
    db.commit()
    db.refresh(john)
    yield john
    db.delete(john)
    db.commit()
