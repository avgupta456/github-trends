import unittest

from models.misc.date import today
from models.user.contribution_stats import UserContribStats
from processing.user.contribution_stats import get_user_contribution_stats


class TestTemplate(unittest.TestCase):
    def test_get_user_contribution_stats(self):
        response = get_user_contribution_stats(user_id="avgupta456")
        self.assertIsInstance(response, UserContribStats)

        response = get_user_contribution_stats(user_id="avgupta456", max_repos=1)
        self.assertLessEqual(len(response.contribs_by_repo), 1)

        start = today - 100
        response = get_user_contribution_stats(user_id="avgupta456", start_date=start)
        date = response.contribs.issues[0].occurred_at
        self.assertGreaterEqual(date - start, 0)
        self.assertGreaterEqual(today - date, 0)
