from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/users/ping")
async def ping():
    a = 5
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
