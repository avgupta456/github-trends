from datetime import datetime, timedelta
import unittest

from src.data.github.graphql import (
    get_user_contribution_years,
    get_user_contribution_calendar,
    get_user_contribution_events,
    get_user_followers,
    get_user_following,
    RawCalendar,
    RawEvents,
    RawFollows,
)

from src.constants import TEST_USER_ID as USER_ID, TEST_TOKEN as TOKEN


class TestTemplate(unittest.TestCase):
    def test_get_user_contribution_years(self):
        response = get_user_contribution_years(user_id=USER_ID, access_token=TOKEN)

        # aside from validating APIResponse class, pydantic will validate tree
        self.assertIsInstance(response, list)

    def test_get_user_contribution_calendar(self):
        response = get_user_contribution_calendar(
            user_id=USER_ID,
            access_token=TOKEN,
            start_date=datetime.today() - timedelta(days=365),
            end_date=datetime.today(),
        )
        self.assertIsInstance(response, RawCalendar)

    def test_get_user_contribution_events(self):
        response = get_user_contribution_events(
            user_id=USER_ID,
            access_token=TOKEN,
            start_date=datetime.today() - timedelta(days=365),
            end_date=datetime.today(),
        )
        self.assertIsInstance(response, RawEvents)

        # TODO: Add more validation here

    def test_get_user_followers(self):
        response = get_user_followers(user_id=USER_ID, access_token=TOKEN)
        self.assertIsInstance(response, RawFollows)

        response = get_user_followers(user_id=USER_ID, access_token=TOKEN, first=1)
        self.assertLessEqual(len(response.nodes), 1)

    def test_get_user_following(self):
        response = get_user_following(user_id=USER_ID, access_token=TOKEN)
        self.assertIsInstance(response, RawFollows)

        response = get_user_following(user_id=USER_ID, access_token=TOKEN, first=1)
        self.assertLessEqual(len(response.nodes), 1)
