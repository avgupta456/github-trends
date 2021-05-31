from datetime import datetime
from typing import Any, Dict, Tuple

import requests
from requests.exceptions import ReadTimeout

from constants import TIMEOUT

s = requests.session()


class GraphQLError(Exception):
    pass


class GraphQLErrorMissingNode(Exception):
    def __init__(self, node: int, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        super(Exception, self).__init__(*args, **kwargs)
        self.node = node


class GraphQLErrorAuth(Exception):
    pass


class GraphQLErrorTimeout(Exception):
    pass


def get_template(query: Dict[str, Any], access_token: str) -> Dict[str, Any]:
    """Template for interacting with the GitHub GraphQL API"""
    start = datetime.now()
    headers: Dict[str, str] = {"Authorization": "bearer " + access_token}

    try:
        r = s.post(  # type: ignore
            "https://api.github.com/graphql",
            json=query,
            headers=headers,
            timeout=TIMEOUT,
        )
    except ReadTimeout:
        raise GraphQLErrorTimeout("GraphQL Error: Request Timeout")

    print("GraphQL", datetime.now() - start)
    if r.status_code == 200:
        data = r.json()  # type: ignore
        if "errors" in data:
            if (
                "type" in data["errors"][0]
                and data["errors"][0]["type"] == "SERVICE_UNAVAILABLE"
                and "path" in data["errors"][0]
                and isinstance(data["errors"][0]["path"], list)
                and len(data["errors"][0]["path"]) == 3  # type: ignore
                and data["errors"][0]["path"][0] == "nodes"
            ):
                raise GraphQLErrorMissingNode(node=int(data["errors"][0]["path"][1]))  # type: ignore
            raise GraphQLError("GraphQL Error: " + str(data["errors"]))
        return data

    if r.status_code == 403:
        raise GraphQLErrorAuth("GraphQL Error: Unauthorized")

    if r.status_code == 502:
        raise GraphQLErrorTimeout("GraphQL Error: Request Timeout")

    raise GraphQLError("GraphQL Error: " + str(r.status_code))
