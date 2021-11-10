import unittest

from src.constants import TEST_TOKEN as TOKEN, TEST_USER_ID as USER_ID
from src.data.github.auth.main import get_unknown_user


class TestTemplate(unittest.TestCase):
    def test_get_unknown_user_valid(self):
        user_id = get_unknown_user(TOKEN)
        self.assertEqual(user_id, USER_ID)

    def test_get_unknown_user_invalid(self):
        user_id = get_unknown_user("")
        self.assertEqual(user_id, None)

    # TODO: test authenticate()
