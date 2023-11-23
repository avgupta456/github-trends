import logging
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import requests
from requests.exceptions import ReadTimeout

from src.constants import TIMEOUT
from src.data.github.utils import get_access_token

s = requests.session()


class GraphQLError(Exception):
    pass


class GraphQLErrorMissingNode(Exception):
    def __init__(self, node: int, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        super(Exception, self).__init__(*args, **kwargs)
        self.node = node


class GraphQLErrorRateLimit(Exception):
    pass


class GraphQLErrorTimeout(Exception):
    pass


def get_template(
    query: Dict[str, Any], access_token: Optional[str] = None, retries: int = 0
) -> Dict[str, Any]:
    """
    Template for interacting with the GitHub GraphQL API
    :param query: The query to be sent to the GitHub GraphQL API
    :param access_token: The access token to be used for the query
    :param retries: The number of retries to be made for Auth Exceptions
    :return: The response from the GitHub GraphQL API
    """
    start = datetime.now()
    new_access_token = get_access_token(access_token)
    headers: Dict[str, str] = {"Authorization": f"bearer {new_access_token}"}

    try:
        r = s.post(
            "https://api.github.com/graphql",
            json=query,
            headers=headers,
            timeout=TIMEOUT,
        )
    except ReadTimeout:
        raise GraphQLErrorTimeout("GraphQL Error: Request Timeout")

    print("GraphQL", new_access_token, datetime.now() - start)
    if r.status_code == 200:
        data = r.json()
        if "errors" in data:
            if (
                "type" in data["errors"][0]
                and data["errors"][0]["type"] in ["SERVICE_UNAVAILABLE", "NOT_FOUND"]
                and "path" in data["errors"][0]
                and isinstance(data["errors"][0]["path"], list)
                and data["errors"][0]["path"][0] == "nodes"
            ):
                raise GraphQLErrorMissingNode(node=int(data["errors"][0]["path"][1]))

            if retries < 2:
                print("GraphQL Error, Retrying:", new_access_token)
                return get_template(query, access_token, retries + 1)

            raise GraphQLError("GraphQL Error: " + str(data["errors"]))

        return data

    if r.status_code in [401, 403]:
        if retries < 2:
            print("GraphQL Error, Retrying:", new_access_token)
            return get_template(query, access_token, retries + 1)
        raise GraphQLErrorRateLimit("GraphQL Error: Unauthorized")

    if r.status_code == 502:
        raise GraphQLErrorTimeout("GraphQL Error: Request Timeout")

    raise GraphQLError(f"GraphQL Error: {str(r.status_code)}")


def get_query_limit(access_token: str) -> int:
    """
    Get the current rate limit for the GitHub GraphQL API
    :param access_token: The access token to be used for the query
    :return: The current rate limit for the GitHub GraphQL API
    """
    try:
        data = get_template(
            {"query": "query { rateLimit { remaining } }"}, access_token
        )
        return data["data"]["rateLimit"]["remaining"]
    except Exception as e:
        logging.exception(e)
        return -1
