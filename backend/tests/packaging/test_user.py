import unittest

from packaging.user import main
from models.user.user import UserPackage


class TestTemplate(unittest.TestCase):
    def test_main(self):
        response = main(user_id="avgupta456")
        self.assertIsInstance(response, UserPackage)
