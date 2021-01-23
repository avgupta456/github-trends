import unittest

from models.user.follows import UserFollows
from processing.user.follows import get_user_followers


class TestTemplate(unittest.TestCase):
    def test_get_user_followers(self):
        response = get_user_followers(user_id="avgupta456")
        self.assertIsInstance(response, UserFollows)
