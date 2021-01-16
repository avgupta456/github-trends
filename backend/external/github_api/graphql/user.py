from external.github_api.graphql.template import get_template


def get_user(user_id: str) -> dict:
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
                        contributions(first: 10){
                        totalCount
                        nodes{
                            commitCount,
                            occurredAt,       	
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

    return get_template(query)
