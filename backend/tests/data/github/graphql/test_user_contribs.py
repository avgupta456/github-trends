import unittest
from datetime import datetime, timedelta

from src.constants import TEST_TOKEN as TOKEN, TEST_USER_ID as USER_ID
from src.data.github.graphql import (
    RawCalendar,
    RawEvents,
    get_user_contribution_calendar,
    get_user_contribution_events,
)


class TestTemplate(unittest.TestCase):
    def test_get_user_contribution_calendar(self):
        response = get_user_contribution_calendar(
            user_id=USER_ID,
            access_token=TOKEN,
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now(),
        )

        self.assertIsInstance(response, RawCalendar)

    def test_get_user_contribution_events(self):
        response = get_user_contribution_events(
            user_id=USER_ID,
            access_token=TOKEN,
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now(),
        )

        self.assertIsInstance(response, RawEvents)
