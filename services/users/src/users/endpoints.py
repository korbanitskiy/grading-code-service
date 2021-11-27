from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .deps import get_db
from .schemas import UserRequest, User
from .crud import create_user, UserAlreadyExistsError, find_user

router = APIRouter()


@router.get("/users/ping")
async def ping():
    return {"message": "pong"}


@router.post("/users", status_code=201)
async def add_user(user: UserRequest, db=Depends(get_db)):
    try:
        user = create_user(db, user)
    except UserAlreadyExistsError:
        return JSONResponse(status_code=400, content=f"User with email {user.email} is already exists")
    else:
        return {"message": f"{user.name} was added"}


@router.get("/users/{user_id}")
async def get_user(user_id: int, db=Depends(get_db), response_model=User):
    user = find_user(db, user_id)
    if not user:
        return JSONResponse(status_code=404, content=f"User {user_id} is not found")
    return user
