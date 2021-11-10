import unittest

from src.constants import TEST_TOKEN as TOKEN, TEST_USER_ID as USER_ID
from src.data.github.graphql import RawFollows, get_user_followers, get_user_following


class TestTemplate(unittest.TestCase):
    def test_get_user_followers(self):
        response = get_user_followers(user_id=USER_ID, access_token=TOKEN)
        self.assertIsInstance(response, RawFollows)

        response = get_user_followers(user_id=USER_ID, access_token=TOKEN, first=1)
        self.assertLessEqual(len(response.nodes), 1)

    def test_get_user_following(self):
        response = get_user_following(user_id=USER_ID, access_token=TOKEN)
        self.assertIsInstance(response, RawFollows)

        response = get_user_following(user_id=USER_ID, access_token=TOKEN, first=1)
        self.assertLessEqual(len(response.nodes), 1)
