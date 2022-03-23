import unittest

from src.constants import TEST_NODE_IDS as NODE_IDS, TEST_TOKEN as TOKEN
from src.data.github.graphql import RawCommit, get_commits


class TestTemplate(unittest.TestCase):
    def test_get_commits(self):
        node_ids = get_commits(access_token=TOKEN, node_ids=NODE_IDS, catch_errors=True)

        # assert returns equal number of commits
        self.assertIsInstance(node_ids, list)
        self.assertEqual(len(node_ids), len(NODE_IDS))

        self.assertIsInstance(node_ids[0], RawCommit)

    def test_get_commits_invalid_access_token(self):
        node_ids = get_commits(access_token="", node_ids=NODE_IDS, catch_errors=True)

        # assert returns list of Nones
        self.assertIsInstance(node_ids, list)
        self.assertEqual(len(node_ids), len(NODE_IDS))
        self.assertIsInstance(node_ids[0], type(None))

    def test_get_commits_invalid_node_ids(self):
        node_ids = get_commits(
            access_token=TOKEN,
            node_ids=[NODE_IDS[0], "", NODE_IDS[1]],
            catch_errors=True,
        )

        self.assertIsInstance(node_ids[0], RawCommit)
        self.assertIsInstance(node_ids[1], type(None))
        self.assertIsInstance(node_ids[2], RawCommit)
