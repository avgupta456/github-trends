from typing import Any, Dict, List

from src.data.github.rest.template import get_template, get_template_plural

BASE_URL = "https://api.github.com/users/"


# TODO: create return classes


def get_user(user_id: str, access_token: str) -> Dict[str, Any]:
    """Returns raw user data"""
    return get_template(BASE_URL + user_id, access_token)


def get_user_starred_repos(
    user_id: str, access_token: str, per_page: int = 100
) -> List[Dict[str, Any]]:
    """Returns list of starred repos"""
    return get_template_plural(
        BASE_URL + user_id + "/starred",
        access_token,
        per_page=per_page,
        accept_header="application/vnd.github.v3.star+json",
    )
