from typing import List, Optional

from src.constants import PR_FILES
from src.data.github.graphql.models import RawCommit
from src.data.github.graphql.template import (
    GraphQLError,
    GraphQLErrorMissingNode,
    GraphQLErrorRateLimit,
    GraphQLErrorTimeout,
    get_template,
)


def get_commits(
    node_ids: List[str], access_token: Optional[str] = None, catch_errors: bool = False
) -> List[Optional[RawCommit]]:
    """
    Gets all repository data from graphql
    :param access_token: GitHub access token
    :param node_ids: List of node ids
    :return: List of commits
    """

    if PR_FILES == 0:  # type: ignore
        query = {
            "variables": {"ids": node_ids},
            "query": """
            query getCommits($ids: [ID!]!) {
                nodes(ids: $ids) {
                    ... on Commit {
                        additions
                        deletions
                        changedFiles
                        url
                    }
                }
            }
            """,
        }
    else:
        query = {
            "variables": {"ids": node_ids, "first": PR_FILES},
            "query": """
            query getCommits($ids: [ID!]!, $first: Int!) {
                nodes(ids: $ids) {
                    ... on Commit {
                        additions
                        deletions
                        changedFiles
                        url
                        associatedPullRequests(first: 1) {
                            nodes {
                                changedFiles
                                additions
                                deletions
                                files(first: $first) {
                                    nodes {
                                        path
                                        additions
                                        deletions
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """,
        }

    try:
        raw_commits = get_template(query, access_token)["data"]["nodes"]
    except GraphQLErrorMissingNode as e:
        return (
            get_commits(node_ids[: e.node], access_token)
            + [None]
            + get_commits(node_ids[e.node + 1 :], access_token)
        )
    except (GraphQLErrorRateLimit, GraphQLErrorTimeout, GraphQLError) as e:
        if catch_errors:
            return [None for _ in node_ids]
        raise e

    out: List[Optional[RawCommit]] = []
    for raw_commit in raw_commits:
        try:
            if "associatedPullRequests" not in raw_commit:
                raw_commit["associatedPullRequests"] = {"nodes": []}
            out.append(RawCommit.model_validate(raw_commit))
        except Exception as e:
            if catch_errors:
                out.append(None)
            else:
                raise e
    return out
