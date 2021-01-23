import unittest

from models.misc.date import today
from models.user.contribution_commits import CommitContributions
from processing.user.contribution_commits import get_user_contribution_commits


class TestTemplate(unittest.TestCase):
    def test_get_user_contribution_commits(self):
        response = get_user_contribution_commits(user_id="avgupta456")
        self.assertIsInstance(response, CommitContributions)

        response = get_user_contribution_commits(user_id="avgupta456", max_repos=1)
        self.assertLessEqual(len(response.commit_contribs_by_repo), 1)

        start = today - 100
        response = get_user_contribution_commits(user_id="avgupta456", start_date=start)
        date = response.commit_contribs_by_repo[0].timeline[0].occurred_at
        self.assertGreaterEqual(date - start, 0)
        self.assertGreaterEqual(today - date, 0)
