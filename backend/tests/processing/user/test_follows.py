import unittest

from models.user.follows import UserFollows
from processing.user.follows import get_user_follows


class TestTemplate(unittest.TestCase):
    def test_get_contributions(self):
        response = get_user_follows("avgupta456")
        self.assertIsInstance(response, UserFollows)

        # TODO: Add further validation
