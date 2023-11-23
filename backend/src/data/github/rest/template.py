from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import ReadTimeout

from src.constants import TIMEOUT
from src.data.github.utils import get_access_token

s = requests.session()


class RESTError(Exception):
    pass


class RESTErrorUnauthorized(RESTError):
    pass


class RESTErrorNotFound(RESTError):
    pass


class RESTErrorEmptyRepo(RESTError):
    pass


class RESTErrorTimeout(RESTError):
    pass


def _get_template(
    query: str,
    params: Dict[str, Any],
    accept_header: str,
    access_token: Optional[str] = None,
    retries: int = 0,
) -> Any:
    """
    Internal template for interacting with the GitHub REST API
    :param query: The query to be sent to the GitHub API
    :param params: The parameters to be sent to the GitHub API
    :param access_token: The access token to be sent to the GitHub API
    :param accept_header: The accept header to be sent to the GitHub API
    :return: The response from the GitHub API
    """
    start = datetime.now()

    new_access_token = get_access_token(access_token)
    headers: Dict[str, str] = {
        "Accept": accept_header,
        "Authorization": f"bearer {new_access_token}",
    }

    try:
        r = s.get(query, params=params, headers=headers, timeout=TIMEOUT)
    except ReadTimeout:
        raise RESTErrorTimeout("REST Error: Request Timeout")

    if r.status_code == 200:
        print("REST API", new_access_token, datetime.now() - start)
        return r.json()

    if r.status_code == 401:
        raise RESTErrorUnauthorized("REST Error: Unauthorized")

    if r.status_code == 404:
        raise RESTErrorNotFound("REST Error: Not Found")

    if r.status_code == 409:
        raise RESTErrorEmptyRepo("REST Error: Empty Repository")

    if retries < 3:
        print("REST Error, Retrying:", new_access_token)
        return _get_template(query, params, accept_header, access_token, retries + 1)
    raise RESTError(f"REST Error: {str(r.status_code)}")


def get_template(
    query: str,
    access_token: Optional[str] = None,
    accept_header: str = "application/vnd.github.v3+json",
) -> Dict[str, Any]:
    """
    Template for interacting with the GitHub REST API (singular)
    :param query: The query to be sent to the GitHub API
    :param access_token: The access token to be sent to the GitHub API
    :param accept_header: The accept header to be sent to the GitHub API
    :return: The response from the GitHub API
    """
    return _get_template(query, {}, accept_header, access_token)


def get_template_plural(
    query: str,
    access_token: Optional[str] = None,
    per_page: int = 100,
    page: int = 1,
    accept_header: str = "application/vnd.github.v3+json",
) -> List[Dict[str, Any]]:
    """
    Template for interacting with the GitHub REST API (plural)
    :param query: The query to be sent to the GitHub API
    :param access_token: The access token to be sent to the GitHub API
    :param per_page: The number of items to be returned per page
    :param page: The page number to be returned
    :param accept_header: The accept header to be sent to the GitHub API
    :return: The response from the GitHub API
    """
    params: Dict[str, str] = {"per_page": str(per_page), "page": str(page)}
    return _get_template(query, params, accept_header, access_token)
