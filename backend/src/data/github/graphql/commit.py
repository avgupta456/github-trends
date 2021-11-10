import logging
from typing import List, Optional

from src.data.github.graphql.models import RawCommit
from src.data.github.graphql.template import (
    GraphQLError,
    GraphQLErrorAuth,
    GraphQLErrorMissingNode,
    GraphQLErrorTimeout,
    get_template,
)


def get_commits(access_token: str, node_ids: List[str]) -> List[Optional[RawCommit]]:
    """
    Gets all repository data from graphql
    :param access_token: GitHub access token
    :param node_ids: List of node ids
    :return: List of commits
    """
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

    try:
        raw_commits = get_template(query, access_token)["data"]["nodes"]
    except GraphQLErrorMissingNode as e:
        return (
            get_commits(access_token, node_ids[: e.node])
            + [None]
            + get_commits(access_token, node_ids[e.node + 1 :])
        )
    except (GraphQLErrorAuth, GraphQLErrorTimeout):
        return [None for _ in node_ids]
    except GraphQLError as e:
        logging.exception(e)
        return [None for _ in node_ids]

    out: List[Optional[RawCommit]] = []
    for raw_commit in raw_commits:
        try:
            out.append(RawCommit.parse_obj(raw_commit))
        except Exception as e:
            logging.exception(e)
            out.append(None)
    return out
