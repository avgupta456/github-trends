import unittest

from src.constants import (
    TEST_REPO as REPO,
    TEST_SHA as SHA,
    TEST_TOKEN as TOKEN,
    TEST_USER_ID as USER_ID,
)
from src.data.github.rest import RawCommitFile, get_commit_files


class TestTemplate(unittest.TestCase):
    def test_get_commit_files(self):
        commits = get_commit_files(
            access_token=TOKEN, owner=USER_ID, repo=REPO, sha=SHA
        )
        self.assertIsInstance(commits, list)
        self.assertIsInstance(commits[0], RawCommitFile)  # type: ignore

    def test_get_commit_files_invalid_access_token(self):
        repo = get_commit_files(access_token="", owner=USER_ID, repo=REPO, sha=SHA)
        self.assertEqual(repo, None)

    def test_get_commit_files_invalid_args(self):
        repo = get_commit_files(access_token=TOKEN, owner="abc123", repo=REPO, sha=SHA)
        self.assertEqual(repo, None)
