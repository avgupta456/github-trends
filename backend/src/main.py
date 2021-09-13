import base64
import json
import logging

from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from google.cloud import pubsub_v1  # type: ignore

from src.external.google_datastore.datastore import get_all_user_ids

load_dotenv()

# flake8: noqa E402

# add endpoints here (after load dotenv)
from src.constants import PUBSUB_PUB, PUBSUB_TOKEN, OAUTH_CLIENT_SECRET

from src.endpoints.user import main as _get_user
from src.endpoints.github_auth import get_access_token

"""
SETUP
"""

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

"""
HELPER FUNCTIONS
"""


@app.get("/")
async def read_root():
    return {"Hello World": [PUBSUB_TOKEN, OAUTH_CLIENT_SECRET]}


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


def async_fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        start = datetime.now()
        try:
            data = await func(response, *args, **kwargs)
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


count: int = 0

publisher = pubsub_v1.PublisherClient()


@app.get("/test", status_code=status.HTTP_200_OK)
@fail_gracefully
def test(response: Response) -> Any:
    return {"test": count}


@app.get("/pubsub/{update}", status_code=status.HTTP_200_OK)
@fail_gracefully
def test_post(response: Response, update: str) -> Any:
    topic_path = publisher.topic_path("github-298920", "test")  # type: ignore

    data = json.dumps({"num": int(update)}).encode("utf-8")

    publisher.publish(topic_path, data=data)  # type: ignore

    return update


@app.post("/push/{token}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def test_pubsub(response: Response, token: str, request: Request) -> Any:
    print(PUBSUB_TOKEN)
    if token != PUBSUB_TOKEN:
        raise HTTPException(400, "Incorrect Token")

    data = await request.json()
    data = json.loads(base64.b64decode(data["message"]["data"]))

    print(data)

    global count
    count += data["num"]


"""
USER LOGIN
"""


@app.post("/login/{code}", status_code=status.HTTP_200_OK)
@fail_gracefully
def login(response: Response, code: str) -> Any:
    if not PUBSUB_PUB:
        raise HTTPException(500, "Login using PUB Server, not SUB Server")
    return get_access_token(code)


"""
ENDPOINTS
"""


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user(response: Response, user_id: str) -> Any:
    return await _get_user(user_id)


@app.get("/user_refresh", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user_refresh(response: Response) -> Any:
    data = get_all_user_ids()
    for user_id in data:
        try:
            await _get_user(user_id, use_cache=False)
        except Exception as e:
            print(e)
    return "Successfully Updated"
