from typing import Any, Dict, List, Union

from external.github_api.graphql.template import get_template


def get_commits(node_ids: List[str]) -> Union[Dict[str, Any], List[Any]]:
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
                    repository{
                        languages(first: 10, orderBy: {field:SIZE, direction:DESC}){
                            totalSize
                            edges{
                                size
                                node{
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
        """,
    }

    return get_template(query)
