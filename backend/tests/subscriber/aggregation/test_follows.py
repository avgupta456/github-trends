import unittest

from src.constants import TEST_TOKEN as TOKEN, TEST_USER_ID as USER_ID
from src.models import UserFollows
from src.processing.layer0 import get_user_follows


class TestTemplate(unittest.TestCase):
    def test_get_follows(self):
        response = get_user_follows(USER_ID, TOKEN)
        self.assertIsInstance(response, UserFollows)

        # TODO: Add further validation
