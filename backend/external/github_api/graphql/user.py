import logging
from typing import Any, Dict

from external.github_api.graphql.template import get_template
from models.user.commit_contributions_by_repository import (
    APIResponse as UserCommitContributionsByRepositoryAPIResponse,
)
from models.user.contribution_calendar import APIResponse as UserContributionCalendar


def get_user(user_id: str) -> Dict[str, Any]:
    """gets all user data from graphql"""
    query = {
        "variables": {"login": user_id},
        "query": """
        query getUser($login: String!) {
            user(login: $login){
                contributionsCollection{
                    commitContributionsByRepository(maxRepositories: 10){
                        repository{
                            name,
                        },
                        totalCount:contributions(first: 1){
                            totalCount
                        }
                        contributions(first: 100){
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
                },
                contributionCalendar{
                    totalContributions,
                    weeks{
                        contributionDays{
                            date,
                            weekday,
                            contributionCount,
                            contributionLevel,
                        }
                    }
                    colors,
                }
                contributionYears,
                issueContributions(first: 10){
                    totalCount,
                    nodes{
                        occurredAt,
                        issue{
                            state
                        }
                    }
                }
                issueContributionsByRepository(maxRepositories: 10){
                    repository{
                        name
                    },
                    contributions(first: 10){
                        totalCount,
                        nodes{
                            occurredAt,
                            issue{
                                state
                            }
                        }
                    }
                }
                pullRequestContributions(first: 10){
                    totalCount,
                    nodes{
                        occurredAt,
                        pullRequest{
                            state
                        }
                    }
                }
                pullRequestContributionsByRepository(maxRepositories:10){
                    repository{
                        name
                    },
                    contributions(first:10){
                        totalCount,
                        nodes{
                            occurredAt,
                            pullRequest{
                                state,
                            }
                        }
                    }
                }
                pullRequestReviewContributions(first: 10){
                    totalCount,
                    nodes{
                        occurredAt,
                        pullRequestReview{
                            state
                        }
                    }
                }
                pullRequestReviewContributionsByRepository(maxRepositories:10){
                    repository{
                        name
                    },
                    contributions(first:10){
                        totalCount,
                        nodes{
                            occurredAt,
                            pullRequestReview{
                                state,
                            }
                        }
                    }
                },
                repositoryContributions(first:10){
                    totalCount,
                    nodes{
                        repository{
                            name,
                        }
                        occurredAt,
                    }
                },
                restrictedContributionsCount,
                totalCommitContributions,
                totalIssueContributions,
                totalPullRequestContributions,
                totalPullRequestReviewContributions,
                totalRepositoryContributions,
                totalRepositoriesWithContributedCommits,
                totalRepositoriesWithContributedIssues,
                totalRepositoriesWithContributedPullRequests,
                totalRepositoriesWithContributedPullRequestReviews
                },
                followers(first:10){
                    totalCount,
                    nodes{
                        name,
                        url,
                    }
                }
                following(first:10){
                    totalCount,
                    nodes{
                        name,
                        url,
                    }
                }
            }
        }
        """,
    }

    try:
        return get_template(query)
    except Exception as e:
        logging.exception(e)
        raise e


def get_user_commit_contributions_by_repository(
    user_id: str,
    max_repos: int = 100,
    first: int = 100,
    after: str = "",
) -> UserCommitContributionsByRepositoryAPIResponse:
    """Runs an individual query, fetching at most 100 days of history"""
    query = {
        "variables": {
            "login": user_id,
            "maxRepos": max_repos,
            "first": first,
            "after": after,
        },
        "query": """
        query getUser($login: String!, $maxRepos: Int!, $first: Int!, $after: String!) {
            user(login: $login){
                contributionsCollection{
                    commitContributionsByRepository(maxRepositories: $maxRepos){
                        repository{
                            name,
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
                },
            },
        }
        """,
    }

    try:
        output_dict = get_template(query)["data"]["user"]["contributionsCollection"][
            "commitContributionsByRepository"
        ]
        return UserCommitContributionsByRepositoryAPIResponse(data=output_dict)
    except Exception as e:
        logging.exception(e)
        raise e


def get_user_contribution_calendar(user_id: str) -> UserContributionCalendar:
    """Fetches user contribution calendar and contribution years"""
    query = {
        "variables": {"login": user_id},
        "query": """
        query getUser($login: String!) {
            user(login: $login){
                contributionsCollection{
                    contributionCalendar{
                        totalContributions,
                        weeks{
                            contributionDays{
                                date,
                                weekday,
                                contributionCount,
                                contributionLevel,
                            }
                        }
                        colors,
                    }
                    contributionYears,
                }
            },
        }
        """,
    }

    try:
        output_dict = get_template(query)["data"]["user"]["contributionsCollection"]
        return UserContributionCalendar.parse_obj(output_dict)
    except Exception as e:
        logging.exception(e)
        raise e
