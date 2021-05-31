from typing import Dict

import requests

s = requests.session()


def get_unknown_user(access_token: str) -> str:
    headers: Dict[str, str] = {
        "Accept": str("application/vnd.github.v3+json"),
        "Authorization": "bearer " + access_token,
    }

    r = s.get("https://api.github.com/user", params={}, headers=headers)
    return r.json()["login"]  # type: ignore
