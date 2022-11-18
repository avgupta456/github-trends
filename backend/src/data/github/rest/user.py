from typing import Any, Dict, List

from src.data.github.rest.template import get_template, get_template_plural

BASE_URL = "https://api.github.com/users/"


def get_user(user_id: str, access_token: str) -> Dict[str, Any]:
    """
    Returns raw user data
    :param user_id: GitHub user id
    :param access_token: GitHub access token
    """
    return get_template(BASE_URL + user_id, access_token)


def get_user_starred_repos(
    user_id: str, access_token: str, per_page: int = 100, page: int = 1
) -> List[Dict[str, Any]]:
    """
    Returns list of starred repos
    :param user_id: GitHub user id
    :param access_token: GitHub access token
    :param per_page: number of repos to return per page
    """
    return get_template_plural(
        BASE_URL + user_id + "/starred",
        access_token,
        per_page=per_page,
        page=page,
        accept_header="application/vnd.github.v3.star+json",
    )
