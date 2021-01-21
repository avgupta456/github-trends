import unittest

from models.user.commit_contributions_by_repository import APIResponse
from external.github_api.graphql.user import get_user_commit_contributions_by_repository


class TestTemplate(unittest.TestCase):
    def test_get_user_commit_contributions_by_repository(self):
        response = get_user_commit_contributions_by_repository(user_id="avgupta456")

        self.assertIsInstance(response, APIResponse)
