from fastapi import FastAPI
from typing import Dict, Any

from dotenv import load_dotenv

from external.github_api.graphql.user import get_user as _get_user
from external.github_api.graphql.repo import get_repo as _get_repo

load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/user/{user_id}")
def get_user(user_id: str) -> dict:
    return _get_user(user_id)


@app.get("/repo/{user_id}/{repo_name}")
def get_repo(user_id: str, repo_name: str) -> Dict[str, Any]:
    return _get_repo(user_id, repo_name)
