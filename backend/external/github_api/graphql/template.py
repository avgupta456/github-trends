import os
from datetime import datetime
from typing import Any, Dict

import requests

s = requests.session()


class GraphQlError(Exception):
    pass


def get_template(query: Dict[str, Any]) -> Dict[str, Any]:
    """Template for interacting with the GitHub GraphQL API"""
    start = datetime.now()
    token = os.getenv("AUTH_TOKEN", "")
    headers: Dict[str, str] = {"Authorization": "bearer " + token}
    # print(query, headers)
    r = s.post(  # type: ignore
        "https://api.github.com/graphql", json=query, headers=headers
    )
    # print(r.status_code)
    print("GraphQL", datetime.now() - start)
    if r.status_code == 200:
        data = r.json()  # type: ignore
        if "errors" in data:
            raise GraphQlError("GraphQL errors: " + str(data["errors"]))
        return data

    try:
        raise GraphQlError(
            "Invalid status code "
            + str(r.status_code)
            + ": "
            + str(r.json()["message"])  # type: ignore
            + " Documentation at "
            + str(r.json()["documentation_url"])  # type: ignore
        )
    except Exception:
        raise GraphQlError("Unknown Error")
