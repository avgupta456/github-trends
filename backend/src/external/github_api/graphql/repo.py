from typing import Any, Dict, List, Union

from src.external.github_api.graphql.template import get_template


def get_repo(
    access_token: str, owner: str, repo: str
) -> Union[Dict[str, Any], List[Any]]:
    """gets all repository data from graphql"""
    query = {
        "variables": {"owner": owner, "repo": repo},
        "query": """
        query getRepo($owner: String!, $repo: String!) {
            repository(owner: $owner, name: $repo) {
                forkCount,
                stargazerCount,
                languages(first: 5){
                    totalCount,
                    totalSize,
                    edges{
                        node {
                            name,
                            color,
                        },
                        size,
                    },
                },
            }
        }
        """,
    }

    return get_template(query, access_token)["data"]["repository"]
