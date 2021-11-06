from datetime import datetime
from typing import Dict, Tuple

import requests

from src.constants import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_REDIRECT_URI

s = requests.session()

# TODO: create return class


def get_unknown_user(access_token: str) -> str:
    headers: Dict[str, str] = {
        "Accept": str("application/vnd.github.v3+json"),
        "Authorization": "bearer " + access_token,
    }

    r = s.get("https://api.github.com/user", params={}, headers=headers)
    return r.json()["login"]  # type: ignore


class OAuthError(Exception):
    pass


async def authenticate(code: str) -> Tuple[str, str]:
    start = datetime.now()

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

    print("OAuth SignUp", datetime.now() - start)
    return user_id, access_token
