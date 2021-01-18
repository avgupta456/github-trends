import logging

from typing import Callable, List, Dict, Any
from functools import wraps

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


def fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    def wrapper(response: Response, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        try:
            data = func(response, *args, **kwargs)
            return {"data": data, "message": "200 OK"}
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"data": [], "message": "Error " + str(e)}

    return wrapper


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
@fail_gracefully
def get_user(response: Response, user_id: str) -> List[Dict[str, Any]]:
    return list(map(lambda x: x.dict(), _get_user(user_id)))


@app.get("/repo/{user_id}/{repo_name}", status_code=status.HTTP_200_OK)
@fail_gracefully
def get_repo(response: Response, user_id: str, repo_name: str) -> Dict[str, Any]:
    return _get_repo(user_id, repo_name)
