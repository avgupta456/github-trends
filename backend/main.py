from fastapi import FastAPI

from external.github_api.user import get_user as _get_user

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/user/{user_id}")
def get_user(user_id: str) -> dict:
    return _get_user(user_id)
