# import json
from typing import Dict, Union

from src.data.github.graphql.template import get_template
from src.data.github.graphql.user.follows.models import RawFollows


def get_user_followers(
    user_id: str, access_token: str, first: int = 100, after: str = ""
) -> RawFollows:
    """gets user's followers and users following'"""

    variables: Dict[str, Union[str, int]] = (
        {"login": user_id, "first": first, "after": after}
        if after != ""
        else {"login": user_id, "first": first}
    )

    query_str: str = (
        """
        query getUser($login: String!, $first: Int!, $after: String!) {
            user(login: $login){
                followers(first: $first, after: $after){
                    nodes{
                        name,
                        login,
                        url
                    }
                    pageInfo{
                        hasNextPage,
                        endCursor
                    }
                }
            }
        }
    """
        if after != ""
        else """
        query getUser($login: String!, $first: Int!) {
            user(login: $login){
                followers(first: $first){
                    nodes{
                        name,
                        login,
                        url
                    }
                    pageInfo{
                        hasNextPage,
                        endCursor
                    }
                }
            }
        }
    """
    )

    query = {
        "variables": variables,
        "query": query_str,
    }

    output_dict = get_template(query, access_token)["data"]["user"]["followers"]
    return RawFollows.parse_obj(output_dict)


def get_user_following(
    user_id: str, access_token: str, first: int = 10, after: str = ""
) -> RawFollows:
    """gets user's followers and users following'"""

    variables: Dict[str, Union[str, int]] = (
        {"login": user_id, "first": first, "after": after}
        if after != ""
        else {"login": user_id, "first": first}
    )

    query_str: str = (
        """
        query getUser($login: String!, $first: Int!, $after: String!) {
            user(login: $login){
                following(first: $first, after: $after){
                    nodes{
                        name,
                        login,
                        url
                    }
                    pageInfo{
                        hasNextPage,
                        endCursor
                    }
                }
            }
        }
    """
        if after != ""
        else """
        query getUser($login: String!, $first: Int!) {
            user(login: $login){
                following(first: $first){
                    nodes{
                        name,
                        login,
                        url
                    }
                    pageInfo{
                        hasNextPage,
                        endCursor
                    }
                }
            }
        }
    """
    )

    query = {
        "variables": variables,
        "query": query_str,
    }

    output_dict = get_template(query, access_token)["data"]["user"]["following"]
    return RawFollows.parse_obj(output_dict)
