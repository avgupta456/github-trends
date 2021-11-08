from typing import Optional

from src.data.github.graphql.models import RawRepo
from src.data.github.graphql.template import get_template


def get_repo(access_token: str, owner: str, repo: str) -> Optional[RawRepo]:
    """gets all repository data from graphql"""
    query = {
        "variables": {"owner": owner, "repo": repo},
        "query": """
        query getRepo($owner: String!, $repo: String!) {
            repository(owner: $owner, name: $repo) {
                isPrivate,
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

    try:
        raw_repo = get_template(query, access_token)["data"]["repository"]
        return RawRepo.parse_obj(raw_repo)
    except Exception:
        return None
