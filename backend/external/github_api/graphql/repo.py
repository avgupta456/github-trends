from typing import Dict, Any

from external.github_api.graphql.template import get_template


def get_repo(owner: str, repo: str) -> Dict[str, Any]:
    """gets all repository data from graphql"""
    query = {
        "variables": {"owner": owner, "repo": repo},
        "query": """
        query getRepo($owner: String!, $repo: String!) { 
            repository(owner: $owner, name: $repo) { 
                createdAt,
                updatedAt,
                forkCount,
                forks(first: 10){
                    nodes{
                        createdAt,
                    },
                },
                stargazerCount,
                stargazers(first: 10){
                    nodes{
                        createdAt,
                    },
                },
                primaryLanguage{
                    name
                },
                languages(first: 5){
                    totalCount,
                    totalSize,
                    edges{
                        node {
                            name,
                        },
                        size,
                    },
                },
            }
        }
        """,
    }

    return get_template(query)
