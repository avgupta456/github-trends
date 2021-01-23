from typing import Any, Dict

from external.github_api.rest.template import get_template

BASE_URL = "https://api.github.com/users/"


def get_user(user_id: str) -> Dict[str, Any]:
    """Returns raw user data"""
    return get_template(BASE_URL + user_id)


def get_user_starred_repos(user_id: str, per_page: int = 100) -> Dict[str, Any]:
    """Returns list of starred repos"""
    return get_template(
        BASE_URL + user_id + "/starred",
        plural=True,
        per_page=per_page,
        accept_header="application/vnd.github.v3.star+json",
    )
