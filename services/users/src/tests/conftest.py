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
    values = dict(name='john', email='john@mail.com', is_active=True)
    john = _create_user(values, db)
    yield john
    db.delete(john)
    db.commit()


@pytest.fixture()
def mary(db):
    values = dict(name='mary', email='mary@mail.com', is_active=False)
    mary = _create_user(values, db)
    yield mary
    db.delete(mary)
    db.commit()


def _create_user(fields, db):
    user = User(**fields)
    db.add(user)
    db.commit()
    db.refresh(user)

    db_fields = fields.copy()
    db_fields['id'] = user.id
    user._fields = fields
    user._db_fields = db_fields
    return user
