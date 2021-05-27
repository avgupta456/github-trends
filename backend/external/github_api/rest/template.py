import os
from datetime import datetime
from typing import Any, Dict, List

import requests


s = requests.session()


class RESTError409(Exception):
    pass


class RESTError(Exception):
    pass


def _get_template(query: str, params: Dict[str, Any], accept_header: str) -> Any:
    """Internal template for interacting with the GitHub REST API"""
    start = datetime.now()

    headers: Dict[str, str] = {
        "Accept": str(accept_header),
        "Authorization": "bearer " + os.getenv("AUTH_TOKEN", ""),
    }

    r = s.get(query, params=params, headers=headers)

    if r.status_code == 200:
        print("REST API", datetime.now() - start)
        return r.json()  # type: ignore

    if r.status_code == 409:
        print("REST ERROR 409")
        raise RESTError409()

    raise RESTError("REST Error " + str(r.status_code))


def get_template(
    query: str,
    accept_header: str = "application/vnd.github.v3+json",
) -> Dict[str, Any]:
    """Template for interacting with the GitHub REST API (singular)"""

    try:
        return _get_template(query, {}, accept_header)
    except Exception as e:
        raise e


def get_template_plural(
    query: str,
    per_page: int = 100,
    page: int = 1,
    accept_header: str = "application/vnd.github.v3+json",
) -> List[Dict[str, Any]]:
    """Template for interacting with the GitHub REST API (plural)"""
    params: Dict[str, str] = {"per_page": str(per_page), "page": str(page)}
    try:
        return _get_template(query, params, accept_header)
    except Exception as e:
        raise e
