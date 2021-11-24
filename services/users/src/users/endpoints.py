from fastapi import APIRouter, Depends

from .deps import get_db
from .schemas import UserRequest
from .crud import create_user

router = APIRouter()


@router.get("/users/ping")
async def ping():
    return {"message": "pong"}


@router.post("/users", status_code=201)
async def add_user(user: UserRequest, db=Depends(get_db)):
    user = create_user(db, user)
    return {"message": f"{user.name} was added"}
