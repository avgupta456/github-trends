from datetime import datetime
from typing import Any, Optional

import logging
import requests

from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from src.db.functions.users import login_user
from src.external.github_auth.auth import get_unknown_user
from src.constants import (
    OAUTH_CLIENT_ID,
    OAUTH_CLIENT_SECRET,
    OAUTH_REDIRECT_URI,
    PUBSUB_PUB,
)
from src.decorators import async_fail_gracefully
from src.utils import get_redirect_url

router = APIRouter()

s = requests.session()


class OAuthError(Exception):
    pass


async def authenticate(code: str) -> str:
    start = datetime.now()
    if not PUBSUB_PUB:
        raise HTTPException(400, "Incorrect Server, must use Publisher")

    params = {
        "client_id": OAUTH_CLIENT_ID,
        "client_secret": OAUTH_CLIENT_SECRET,
        "code": code,
        "redirect_uri": OAUTH_REDIRECT_URI,
    }

    r = s.post("https://github.com/login/oauth/access_token", params=params)

    if r.status_code != 200:
        raise OAuthError("OAuth Error: " + str(r.status_code))

    access_token = r.text.split("&")[0].split("=")[1]
    user_id = get_unknown_user(access_token)

    await login_user(user_id, access_token)

    print("OAuth SignUp", datetime.now() - start)
    return user_id


@router.post("/login/{code}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def authenticate_endpoint(response: Response, code: str) -> Any:
    return await authenticate(code)


@router.get("/signup/public")
def redirect_public(user_id: Optional[str] = None) -> Any:
    return RedirectResponse(get_redirect_url(private=False, user_id=user_id))


@router.get("/singup/private")
def redirect_private(user_id: Optional[str] = None) -> Any:
    return RedirectResponse(get_redirect_url(private=True, user_id=user_id))


@router.get("/redirect")
async def redirect_return(code: str = "") -> str:
    try:
        user_id = await authenticate(code=code)  # type: ignore
        return (
            "Authenticated "
            + user_id
            + "! Please continue following instructions in the README."
        )
    except Exception as e:
        logging.exception(e)
        return "Unknown Error. Please try again later."
