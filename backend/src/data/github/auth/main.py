from datetime import datetime
from typing import Dict, Optional, Tuple

import requests

from src.constants import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_REDIRECT_URI

s = requests.session()


def get_unknown_user(access_token: str) -> Optional[str]:
    """
    Accepts access_token and returns user_id of associated user
    :param access_token: GitHub access token
    :return: user_id or None if invalid access_token
    """
    headers: Dict[str, str] = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"bearer {access_token}",
    }

    r = s.get("https://api.github.com/user", params={}, headers=headers)
    return r.json().get("login", None)


class OAuthError(Exception):
    pass


async def authenticate(code: str) -> Tuple[str, str]:
    """
    Takes a authentication code, verifies, and returns user_id/access_token
    :param code: GitHub authentication code from OAuth process
    :return: user_id, access_token of authenticated user
    """
    start = datetime.now()

    params = {
        "client_id": OAUTH_CLIENT_ID,
        "client_secret": OAUTH_CLIENT_SECRET,
        "code": code,
        "redirect_uri": OAUTH_REDIRECT_URI,
    }

    r = s.post("https://github.com/login/oauth/access_token", params=params)

    if r.status_code != 200:
        raise OAuthError(f"OAuth Error: {str(r.status_code)}")

    access_token = r.text.split("&")[0].split("=")[1]
    user_id = get_unknown_user(access_token)

    if user_id is None:
        raise OAuthError("OAuth Error: Invalid user_id/access_token")

    print("OAuth SignUp", datetime.now() - start)
    return user_id, access_token
