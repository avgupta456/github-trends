import unittest

from src.models.user.follows import UserFollows

from src.processing.user.follows import get_user_follows

from src.constants import TEST_USER_ID as USER_ID, TEST_TOKEN as TOKEN


class TestTemplate(unittest.TestCase):
    def test_get_contributions(self):
        response = get_user_follows(USER_ID, TOKEN)
        self.assertIsInstance(response, UserFollows)

        # TODO: Add further validation
