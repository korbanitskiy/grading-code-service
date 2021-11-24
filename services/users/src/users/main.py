import uvicorn
from fastapi import FastAPI

from users.endpoints import router
from users.models import Base
from users.database import engine

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
