# import json
from datetime import datetime
from typing import Optional

from src.data.github.graphql.template import get_template
from src.data.github.graphql.user.contribs.models import RawCalendar, RawEvents


def get_user_contribution_calendar(
    user_id: str,
    start_date: datetime,
    end_date: datetime,
    access_token: Optional[str] = None,
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
                    }
                }
            }
        }
        """,
    }

    raw_data = get_template(query, access_token)
    output = raw_data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return RawCalendar.model_validate(output)


def get_user_contribution_events(
    user_id: str,
    start_date: datetime,
    end_date: datetime,
    max_repos: int = 100,
    first: int = 100,
    after: str = "",
    access_token: Optional[str] = None,
) -> RawEvents:
    """Fetches user contributions (commits, issues, prs, reviews)"""
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
    return RawEvents.model_validate(output)
