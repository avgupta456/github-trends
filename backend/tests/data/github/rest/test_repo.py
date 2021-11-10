import unittest

from src.constants import (
    TEST_REPO as REPO,
    TEST_TOKEN as TOKEN,
    TEST_USER_ID as USER_ID,
)
from src.data.github.rest import RawCommit, get_repo_commits


class TestTemplate(unittest.TestCase):
    def test_get_repo_commits(self):
        commits = get_repo_commits(access_token=TOKEN, owner=USER_ID, repo=REPO)
        self.assertIsInstance(commits, list)
        self.assertIsInstance(commits[0], RawCommit)

    def test_get_repo_commits_invalid_access_token(self):
        repo = get_repo_commits(access_token="", owner=USER_ID, repo=REPO)
        self.assertEqual(repo, [])

    def test_get_repo_commits_invalid_args(self):
        repo = get_repo_commits(access_token=TOKEN, owner="abc123", repo=REPO)
        self.assertEqual(repo, [])
