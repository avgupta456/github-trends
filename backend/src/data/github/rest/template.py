from datetime import datetime
from typing import Any, Dict, List

import requests
from requests.exceptions import ReadTimeout

from src.constants import TIMEOUT


s = requests.session()


class RESTError(Exception):
    pass


class RESTErrorEmptyRepo(Exception):
    pass


class RESTErrorTimeout(Exception):
    pass


def _get_template(
    query: str, params: Dict[str, Any], access_token: str, accept_header: str
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

    headers: Dict[str, str] = {
        "Accept": str(accept_header),
        "Authorization": "bearer " + access_token,
    }

    try:
        r = s.get(query, params=params, headers=headers, timeout=TIMEOUT)
    except ReadTimeout:
        raise RESTErrorTimeout("REST Error: Request Timeout")

    if r.status_code == 200:
        print("REST API", datetime.now() - start)
        return r.json()  # type: ignore

    if r.status_code == 409:
        raise RESTErrorEmptyRepo("REST Error: Empty Repository")

    raise RESTError("REST Error: " + str(r.status_code))


def get_template(
    query: str,
    access_token: str,
    accept_header: str = "application/vnd.github.v3+json",
) -> Dict[str, Any]:
    """
    Template for interacting with the GitHub REST API (singular)
    :param query: The query to be sent to the GitHub API
    :param access_token: The access token to be sent to the GitHub API
    :param accept_header: The accept header to be sent to the GitHub API
    :return: The response from the GitHub API
    """

    try:
        return _get_template(query, {}, access_token, accept_header)
    except Exception as e:
        raise e


def get_template_plural(
    query: str,
    access_token: str,
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
    try:
        return _get_template(query, params, access_token, accept_header)
    except Exception as e:
        raise e
