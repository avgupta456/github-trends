import unittest

from models.user.contribution_calendar import (
    APIResponse as UserContributionCalendarAPIResponse,
)
from models.user.contribution_commits import (
    APIResponse as UserContributionCommitsAPIResponse,
)
from models.user.contribution_stats import (
    APIResponse as UserContributionStatsAPIResponse,
)
from models.user.followers import APIResponse as UserFollowAPIResponse
from external.github_api.graphql.user import (
    get_user_contribution_calendar,
    get_user_contribution_commits,
    get_user_contribution_stats,
    get_user_followers,
    get_user_following,
)


class TestTemplate(unittest.TestCase):
    def test_get_user_contribution_calendar(self):
        response = get_user_contribution_calendar(user_id="avgupta456")

        # aside from validating APIResponse class, pydantic will validate tree
        self.assertIsInstance(response, UserContributionCalendarAPIResponse)

    def test_get_user_contribution_commits(self):
        response = get_user_contribution_commits(user_id="avgupta456")
        self.assertIsInstance(response, UserContributionCommitsAPIResponse)

        response = get_user_contribution_commits(user_id="avgupta456", max_repos=1)
        self.assertLessEqual(len(response.commits_by_repo), 1)

        response = get_user_contribution_commits(user_id="avgupta456", first=1)
        self.assertLessEqual(len(response.commits_by_repo[0].contributions.nodes), 1)

    def test_get_user_contribution_stats(self):
        response = get_user_contribution_stats(user_id="avgupta456")
        self.assertIsInstance(response, UserContributionStatsAPIResponse)

        response = get_user_contribution_stats(user_id="avgupta456", max_repos=1)
        self.assertLessEqual(len(response.issue_contribs_by_repo), 1)

        response = get_user_contribution_stats(user_id="avgupta456", first=1)
        self.assertLessEqual(
            len(response.issue_contribs_by_repo[0].contributions.nodes), 1
        )

    def test_get_user_followers(self):
        response = get_user_followers(user_id="avgupta456")
        self.assertIsInstance(response, UserFollowAPIResponse)

        response = get_user_followers(user_id="avgupta456", first=1)
        self.assertLessEqual(len(response.nodes), 1)

    def test_get_user_following(self):
        response = get_user_following(user_id="avgupta456")
        self.assertIsInstance(response, UserFollowAPIResponse)

        response = get_user_following(user_id="avgupta456", first=1)
        self.assertLessEqual(len(response.nodes), 1)
