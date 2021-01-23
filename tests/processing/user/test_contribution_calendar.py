import unittest

from models.misc.date import today
from models.user.contribution_calendar import ContributionCalendar
from processing.user.contribution_calendar import get_user_contribution_calendar


class TestTemplate(unittest.TestCase):
    def test_get_user_contribution_calendar(self):
        response = get_user_contribution_calendar(user_id="avgupta456")
        self.assertIsInstance(response, ContributionCalendar)

        start = today - 100
        response = get_user_contribution_calendar(
            user_id="avgupta456", start_date=start
        )
        date = response.total.days[0].date
        self.assertGreaterEqual(date - start, 0)
        self.assertGreaterEqual(today - date, 0)
