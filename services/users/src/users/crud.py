from .models import User
from .schemas import UserRequest


def create_user(db, user: UserRequest):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise UserAlreadyExistsError()

    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, id: int):
    user = db.query(User).filter(User.id == id).first()
    return user


class UserAlreadyExistsError(Exception):
    pass
