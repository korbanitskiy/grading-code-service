from pydantic import BaseModel


class UserRequest(BaseModel):
    name: str
    email: str
    is_active: bool
