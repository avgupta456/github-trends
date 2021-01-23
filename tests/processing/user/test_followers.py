import unittest

from models.user.followers import UserFollowers
from processing.user.followers import get_user_followers


class TestTemplate(unittest.TestCase):
    def test_get_user_followers(self):
        response = get_user_followers(user_id="avgupta456")
        self.assertIsInstance(response, UserFollowers)
