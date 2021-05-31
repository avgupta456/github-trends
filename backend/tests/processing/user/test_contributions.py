import unittest

from models.user.contribs import UserContributions

from processing.user.contributions import get_contributions

from constants import TOKEN


class TestTemplate(unittest.TestCase):
    def test_get_contributions(self):
        response = get_contributions("avgupta456", TOKEN)
        self.assertIsInstance(response, UserContributions)

        # TODO: Add further validation
