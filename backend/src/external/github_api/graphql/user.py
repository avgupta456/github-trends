# import json
from typing import Dict, List, Union
from datetime import datetime, timedelta

from src.external.github_api.graphql.template import get_template

from src.models.user.contribs import RawCalendar, RawEvents
from src.models.user.follows import RawFollows


def get_user_contribution_years(user_id: str, access_token: str) -> List[int]:
    """Gets years where the user had activity"""
    query = {
        "variables": {"login": user_id},
        "query": """
        query getUser($login: String!) {
            user(login: $login){
                contributionsCollection{
                    contributionYears
                }
            }
        }
        """,
    }

    raw_data = get_template(query, access_token)
    years = raw_data["data"]["user"]["contributionsCollection"]["contributionYears"]
    return years


def get_user_contribution_calendar(
    user_id: str,
    access_token: str,
    start_date: datetime = datetime.now() - timedelta(days=365),
    end_date: datetime = datetime.now(),
) -> RawCalendar:
    """Gets contribution calendar for a given time period (max one year)"""
    if (end_date - start_date).days > 365:
        raise ValueError("date range can be at most 1 year")
    query = {
        "variables": {
            "login": user_id,
            "startDate": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endDate": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "query": """
        query getUser($login: String!, $startDate: DateTime!, $endDate: DateTime!){
            user(login: $login){
                contributionsCollection(from: $startDate, to: $endDate){
                    contributionCalendar{
                        weeks{
                            contributionDays{
                                date
                                weekday
                                contributionCount
                            }
                        }
                        totalContributions
                    }
                }
            }
        }
        """,
    }

    raw_data = get_template(query, access_token)
    output = raw_data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return RawCalendar.parse_obj(output)


def get_user_contribution_events(
    user_id: str,
    access_token: str,
    start_date: datetime = datetime.now() - timedelta(365),
    end_date: datetime = datetime.now(),
    max_repos: int = 100,
    first: int = 100,
    after: str = "",
) -> RawEvents:
    """Fetches user contributions (commits, issues, prs, reviews)"""
    if (end_date - start_date).days > 365:
        raise ValueError("date range can be at most 1 year")
    query = {
        "variables": {
            "login": user_id,
            "startDate": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endDate": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "maxRepos": max_repos,
            "first": first,
            "after": after,
        },
        "query": """
        query getUser($login: String!, $startDate: DateTime!, $endDate: DateTime!, $maxRepos: Int!, $first: Int!, $after: String!) {
            user(login: $login){
                contributionsCollection(from: $startDate, to: $endDate){
                    commitContributionsByRepository(maxRepositories: $maxRepos){
                        repository{
                            nameWithOwner,
                        },
                        totalCount:contributions(first: 1){
                            totalCount
                        }
                        contributions(first: $first, after: $after){
                            nodes{
                                commitCount,
                                occurredAt,
                            }
                            pageInfo{
                                hasNextPage,
                                endCursor
                            }
                        }
                    }
                    issueContributionsByRepository(maxRepositories: $maxRepos){
                        repository{
                            nameWithOwner
                        },
                        totalCount:contributions(first: 1){
                            totalCount
                        }
                        contributions(first: $first, after: $after){
                            nodes{
                                occurredAt,
                            }
                            pageInfo{
                                hasNextPage,
                                endCursor
                            }
                        }
                    }
                    pullRequestContributionsByRepository(maxRepositories: $maxRepos){
                        repository{
                            nameWithOwner
                        },
                        totalCount:contributions(first: 1){
                            totalCount
                        }
                        contributions(first: $first, after: $after){
                            nodes{
                                occurredAt,
                            }
                            pageInfo{
                                hasNextPage,
                                endCursor
                            }
                        }
                    }
                    pullRequestReviewContributionsByRepository(maxRepositories: $maxRepos){
                        repository{
                            nameWithOwner
                        },
                        totalCount:contributions(first: 1){
                            totalCount
                        }
                        contributions(first: $first, after: $after){
                            nodes{
                                occurredAt,
                            }
                            pageInfo{
                                hasNextPage,
                                endCursor
                            }
                        }
                    },
                    repositoryContributions(first: $maxRepos){
                        totalCount
                        nodes{
                            repository{
                                nameWithOwner,
                            }
                            occurredAt,
                        }
                    },
                },
            }
        }
        """,
    }

    raw_data = get_template(query, access_token)
    output = raw_data["data"]["user"]["contributionsCollection"]
    return RawEvents.parse_obj(output)


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
