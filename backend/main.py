import logging
from typing import Dict, Any

from fastapi import FastAPI, Response, status
from dotenv import load_dotenv

from processing.user.commit_contributions_by_repository import (
    get_user_commit_contributions_by_repository as _get_user,
)
from external.github_api.graphql.repo import get_repo as _get_repo

load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: str, response: Response) -> Dict[str, Any]:
    try:
        data = list(map(lambda x: x.dict(), _get_user(user_id)))
        return {"data": data, "message": ""}
    except Exception as e:
        logging.exception(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"data": [], "message": str(e)}


@app.get("/repo/{user_id}/{repo_name}", status_code=status.HTTP_200_OK)
def get_repo(user_id: str, repo_name: str, response: Response) -> Dict[str, Any]:
    try:
        data = _get_repo(user_id, repo_name)
        return {"data": data, "message": ""}
    except Exception as e:
        logging.exception(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"data": [], "message": str(e)}
