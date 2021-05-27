import os
from datetime import datetime
from typing import Any, Dict

import requests

s = requests.session()


class GraphQLError(Exception):
    pass


class GraphQLError403(Exception):
    pass


def get_template(query: Dict[str, Any]) -> Dict[str, Any]:
    """Template for interacting with the GitHub GraphQL API"""
    start = datetime.now()
    token = os.getenv("AUTH_TOKEN", "")
    headers: Dict[str, str] = {"Authorization": "bearer " + token}
    r = s.post(  # type: ignore
        "https://api.github.com/graphql", json=query, headers=headers
    )
    print("GraphQL", datetime.now() - start)
    if r.status_code == 200:
        data = r.json()  # type: ignore
        if "errors" in data:
            raise GraphQLError("GraphQL Error: " + str(data["errors"]))
        return data

    if r.status_code == 403:
        raise GraphQLError403("GraphQL Error 403: Unauthorized")

    raise GraphQLError("GraphQL Error " + str(r.status_code))
