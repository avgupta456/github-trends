import logging
from typing import Any, Dict

from external.github_api.graphql.template import get_template
from models.user.contribution_commits import (
    APIResponse as UserContributionCommitsAPIResponse,
)
from models.user.contribution_calendar import (
    APIResponse as UserContributionCalendarAPIResponse,
)
from models.user.contribution_stats import (
    APIResponse as UserContributionStatsAPIResponse,
)


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


def get_user_contribution_commits(
    user_id: str,
    max_repos: int = 100,
    first: int = 100,
    after: str = "",
) -> UserContributionCommitsAPIResponse:
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
                    totalCommitContributions,
                    totalRepositoriesWithContributedCommits,
                },
            },
        }
        """,
    }

    try:
        output_dict = get_template(query)["data"]["user"]["contributionsCollection"]
        return UserContributionCommitsAPIResponse.parse_obj(output_dict)
    except Exception as e:
        logging.exception(e)
        raise e


def get_user_contribution_calendar(user_id: str) -> UserContributionCalendarAPIResponse:
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
        return UserContributionCalendarAPIResponse.parse_obj(output_dict)
    except Exception as e:
        logging.exception(e)
        raise e


def get_user_contribution_stats(
    user_id: str,
    max_repos: int = 100,
    first: int = 100,
    after: str = "",
) -> Any:
    """Fetches user contribution calendar and contribution years"""
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
                    issueContributionsByRepository(maxRepositories: $maxRepos){
                        repository{
                            name
                        },
                        contributions(first: $first, after: $after){
                            totalCount,
                            nodes{
                                occurredAt,
                                issue{
                                    state
                                }
                            }
                            pageInfo{
                                hasNextPage,
                                endCursor
                            }
                        }
                    }
                    pullRequestContributionsByRepository(maxRepositories: $maxRepos){
                        repository{
                            name
                        },
                        contributions(first: $first, after: $after){
                            totalCount,
                            nodes{
                                occurredAt,
                                pullRequest{
                                    state,
                                }
                            }
                            pageInfo{
                                hasNextPage,
                                endCursor
                            }
                        }
                    }
                    pullRequestReviewContributionsByRepository(maxRepositories: $maxRepos){
                        repository{
                            name
                        },
                        contributions(first: $first, after: $after){
                            totalCount,
                            nodes{
                                occurredAt,
                                pullRequestReview{
                                    state,
                                }
                            }
                            pageInfo{
                                hasNextPage,
                                endCursor
                            }
                        }
                    },
                    repositoryContributions(first: $first, after: $after){
                        totalCount,
                        nodes{
                            repository{
                                name,
                            }
                            occurredAt,
                        }
                        pageInfo{
                            hasNextPage,
                            endCursor
                        }
                    },
                    restrictedContributionsCount,
                    totalIssueContributions,
                    totalPullRequestContributions,
                    totalPullRequestReviewContributions,
                    totalRepositoryContributions,
                    totalRepositoriesWithContributedIssues,
                    totalRepositoriesWithContributedPullRequests,
                    totalRepositoriesWithContributedPullRequestReviews
                },
            }
        }
        """,
    }

    try:
        output_dict = get_template(query)["data"]["user"]["contributionsCollection"]
        return UserContributionStatsAPIResponse.parse_obj(output_dict)
    except Exception as e:
        logging.exception(e)
        raise e
