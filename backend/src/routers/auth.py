from datetime import datetime
from typing import Any, Optional

import logging
import requests

from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from src.db.user.functions import delete_user, login_user
from src.external.github_auth.auth import get_unknown_user
from src.constants import (
    BACKEND_URL,
    OAUTH_CLIENT_ID,
    OAUTH_CLIENT_SECRET,
    OAUTH_REDIRECT_URI,
    PUBSUB_PUB,
)
from src.helper.decorators import async_fail_gracefully
from src.helper.utils import get_redirect_url

router = APIRouter()

s = requests.session()


class OAuthError(Exception):
    pass


async def authenticate(code: str, private_access: bool = False) -> str:
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

    await login_user(user_id, access_token, private_access)

    print("OAuth SignUp", datetime.now() - start)
    return user_id


@router.post("/login/{code}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def authenticate_endpoint(
    response: Response, code: str, private_access: bool = False
) -> str:
    return await authenticate(code, private_access)


# TODO: reset cache upon upgrade, downgrade, or delete


@router.get("/signup/public")
def redirect_public(user_id: Optional[str] = None) -> RedirectResponse:
    return RedirectResponse(get_redirect_url(private=False, user_id=user_id))


@router.get("/signup/private")
def redirect_private(user_id: Optional[str] = None) -> RedirectResponse:
    return RedirectResponse(get_redirect_url(private=True, user_id=user_id))


@router.get("/redirect")
async def redirect_return(
    code: str = "", private_access: bool = False
) -> RedirectResponse:
    try:
        user_id = await authenticate(code=code, private_access=private_access)  # type: ignore
        return RedirectResponse(BACKEND_URL + "/auth/redirect_success/" + user_id)
    except Exception as e:
        logging.exception(e)
        return RedirectResponse(BACKEND_URL + "/auth/redirect_failure")


@router.get("/redirect_success/{user_id}")
def redirect_success(user_id: str) -> str:
    return "You (" + user_id + ") are now authenticated!"


@router.get("/redirect_failure")
def redirect_failure() -> str:
    return "Unknown Error. Please try again later."


@router.get("/delete/{user_id}")
async def delete_account_auth(user_id: str, redirect: bool = True) -> Any:
    if redirect:
        return RedirectResponse(
            get_redirect_url(prefix="delete/" + user_id, private=False, user_id=user_id)
        )

    # TODO: setup CORS by route to allow adding "await delete_user(user_id)" without security concerns

    await delete_user(user_id)
    return "https://github.com/settings/connections/applications/" + OAUTH_CLIENT_ID


@router.get("/redirect/delete/{user_id}")
async def delete_account(user_id: str) -> RedirectResponse:
    await delete_user(user_id)
    return RedirectResponse(
        "https://github.com/settings/connections/applications/" + OAUTH_CLIENT_ID
    )
