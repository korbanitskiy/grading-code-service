from pydantic import BaseModel


class UserFields(BaseModel):
    name: str
    email: str
    is_active: bool


class UserRequest(UserFields):
    pass


class User(UserFields):
    id: int

    class Config:
        orm_mode = True
