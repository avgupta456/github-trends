from typing import Any, Dict, List, Union

from src.external.github_api.graphql.template import get_template


def get_commits(
    access_token: str, node_ids: List[str]
) -> Union[Dict[str, Any], List[Any]]:
    """gets all repository data from graphql"""
    query = {
        "variables": {"ids": node_ids},
        "query": """
        query getCommits($ids: [ID!]!) {
            nodes(ids: $ids) {
                ... on Commit {
                    additions
                    deletions
                    changedFiles
                }
            }
        }
        """,
    }

    return get_template(query, access_token)["data"]["nodes"]
