from .models import User
from .schemas import UserRequest


def find_all_users(db):
    qs = db.query(User)
    return qs.all()


def find_user(db, user_id: int):
    user_qs = db.query(User).filter(User.id == user_id)
    return user_qs.first()


def create_user(db, user: UserRequest):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise UserAlreadyExistsError()

    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


class UserAlreadyExistsError(Exception):
    pass
