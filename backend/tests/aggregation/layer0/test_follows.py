import unittest

from src.aggregation.layer0.follows import get_user_follows
from src.constants import TEST_TOKEN as TOKEN, TEST_USER_ID as USER_ID
from src.models import UserFollows


class TestTemplate(unittest.TestCase):
    def test_get_follows(self):
        response = get_user_follows(USER_ID, TOKEN)
        self.assertIsInstance(response, UserFollows)

        # TODO: Add further validation
