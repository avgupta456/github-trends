import unittest

from src.data.github.auth.main import get_unknown_user
from src.constants import TEST_USER_ID as USER_ID, TEST_TOKEN as TOKEN


class TestTemplate(unittest.TestCase):
    def test_get_unknown_user_valid(self):
        user_id = get_unknown_user(TOKEN)
        self.assertEqual(user_id, USER_ID)

    def test_get_unknown_user_invalid(self):
        user_id = get_unknown_user("")
        self.assertEqual(user_id, None)

    # TODO: test authenticate()
