import unittest

from src.data.github.graphql import get_repo, RawRepo

from src.constants import (
    TEST_TOKEN as TOKEN,
    TEST_USER_ID as USER_ID,
    TEST_REPO as REPO,
)


class TestTemplate(unittest.TestCase):
    def test_get_repo(self):
        repo: RawRepo = get_repo(access_token=TOKEN, owner=USER_ID, repo=REPO)  # type: ignore

        # assert returns equal number of commits
        self.assertIsInstance(repo, RawRepo)
        self.assertEqual(repo.is_private, False)
        self.assertGreater(repo.fork_count, 0)
        self.assertGreater(repo.stargazer_count, 0)

    def test_get_repo_invalid_access_token(self):
        repo = get_repo(access_token="", owner=USER_ID, repo=REPO)

        # assert returns None
        self.assertIsInstance(repo, type(None))

    def test_get_commits_invalid_args(self):
        repo = get_repo(access_token=TOKEN, owner="abc123", repo=REPO)

        self.assertIsInstance(repo, type(None))
