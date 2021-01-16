import os
import requests

from typing import Optional

s = requests.session()


class GraphQlError(Exception):
    pass


def get_template(query: dict) -> dict:
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Authorization": "bearer " + token}
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
