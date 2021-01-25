import unittest

from models.user.contribs import UserContributions
from processing.user.contributions import get_contributions


class TestTemplate(unittest.TestCase):
    def test_get_contributions(self):
        response = get_contributions("avgupta456")
        self.assertIsInstance(response, UserContributions)

        # TODO: Add further validation
