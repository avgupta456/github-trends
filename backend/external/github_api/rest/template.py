# type: ignore[reportUnknownMemberType]

import requests

from typing import Optional, Dict, Any

s = requests.session()


class RESTError(Exception):
    pass


def get_template(
    query: str,
    plural: Optional[bool] = False,
    per_page: Optional[int] = 100,
    accept_header: Optional[str] = "application/vnd.github.v3+json",
) -> Dict[str, Any]:
    """Template for interacting with the GitHub REST API"""
    headers: Dict[str, str] = {"Accept": accept_header}
    params: Dict[str, str] = {"per_page": str(per_page)} if plural else {}
    r = s.get(query, params=params, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise RESTError(
            "Invalid status code "
            + str(r.status_code)
            + ": "
            + str(r.json()["message"])
            + " Documentation at "
            + str(r.json()["documentation_url"])
        )
