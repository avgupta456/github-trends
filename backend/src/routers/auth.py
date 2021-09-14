from datetime import datetime
from typing import Any

import requests

from fastapi import APIRouter, Response, status

from src.db.functions.users import login_user
from src.external.github_auth.auth import get_unknown_user
from src.constants import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_REDIRECT_URI
from src.utils import async_fail_gracefully

router = APIRouter()

s = requests.session()


class OAuthError(Exception):
    pass


@router.post("/login/{code}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def login(response: Response, code: str) -> Any:
    start = datetime.now()

    params = {
        "client_id": OAUTH_CLIENT_ID,
        "client_secret": OAUTH_CLIENT_SECRET,
        "code": code,
        "redirect_uri": OAUTH_REDIRECT_URI,
    }

    r = s.post("https://github.com/login/oauth/access_token", params=params)  # type: ignore

    if r.status_code == 200:
        access_token = r.text.split("&")[0].split("=")[1]
        user_id = get_unknown_user(access_token)
        await login_user(user_id, access_token)
        print("OAuth API", datetime.now() - start)
        return user_id

    raise OAuthError("OAuth Error: " + str(r.status_code))
