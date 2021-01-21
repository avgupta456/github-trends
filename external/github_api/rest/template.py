from datetime import datetime
from typing import Any, Dict

import requests

s = requests.session()


class RESTError(Exception):
    pass


def get_template(
    query: str,
    plural: bool = False,
    per_page: int = 100,
    accept_header: str = "application/vnd.github.v3+json",
) -> Dict[str, Any]:
    """Template for interacting with the GitHub REST API"""
    start = datetime.now()
    headers: Dict[str, str] = {"Accept": str(accept_header)}
    params: Dict[str, str] = {"per_page": str(per_page)} if plural else {}
    r = s.get(query, params=params, headers=headers)  # type: ignore
    if r.status_code == 200:
        print("REST API", datetime.now() - start)
        return r.json()  # type: ignore
    else:
        raise RESTError(
            "Invalid status code "
            + str(r.status_code)
            + ": "
            + str(r.json()["message"])  # type: ignore
            + " Documentation at "
            + str(r.json()["documentation_url"])  # type: ignore
        )
