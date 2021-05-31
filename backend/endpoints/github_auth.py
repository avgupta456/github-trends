from datetime import datetime
from typing import Any

import requests

from constants import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_REDIRECT_URI
from external.github_auth.auth import get_unknown_user
from external.google_datastore.datastore import set_access_token


s = requests.session()


class OAuthError(Exception):
    pass


def get_access_token(code: str) -> Any:
    """Request a user's access token using code"""

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
        set_access_token(user_id, access_token)
        print("OAuth API", datetime.now() - start)
        return user_id

    raise OAuthError("OAuth Error: " + str(r.status_code))
