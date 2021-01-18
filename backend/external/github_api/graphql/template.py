# type: ignore[reportUnknownMemberType]

import os
import requests

from typing import Dict, Any


s = requests.session()


class GraphQlError(Exception):
    pass


def get_template(query: Dict[str, Any]) -> Dict[str, Any]:
    """Template for interacting with the GitHub GraphQL API"""
    token = os.getenv("GITHUB_TOKEN", "")
    headers: Dict[str, str] = {"Authorization": "bearer " + token}
    r = s.post("https://api.github.com/graphql", json=query, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise GraphQlError(
            "Invalid status code "
            + str(r.status_code)
            + ": "
            + str(r.json()["message"])
            + " Documentation at "
            + str(r.json()["documentation_url"])
        )
