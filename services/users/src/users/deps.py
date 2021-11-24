from .database import DBSession


def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
