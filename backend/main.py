import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from endpoints.user import main as _get_user

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


def fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    def wrapper(response: Response, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        start = datetime.now()
        try:
            data = func(response, *args, **kwargs)
            return {"data": data, "message": "200 OK", "time": datetime.now() - start}
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "data": [],
                "message": "Error " + str(e),
                "time": datetime.now() - start,
            }

    return wrapper


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
@fail_gracefully
def get_user(response: Response, user_id: str) -> Any:
    return _get_user(user_id)
