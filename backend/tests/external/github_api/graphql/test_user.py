import unittest

from models.user.contribs import RawCalendar, RawEvents
from models.user.follows import RawFollows
from external.github_api.graphql.user import (
    get_user_contribution_years,
    get_user_contribution_calendar,
    get_user_contribution_events,
    get_user_followers,
    get_user_following,
)

from constants import USER_ID, TOKEN


class TestTemplate(unittest.TestCase):
    def test_get_user_contribution_years(self):
        response = get_user_contribution_years(user_id=USER_ID, access_token=TOKEN)

        # aside from validating APIResponse class, pydantic will validate tree
        self.assertIsInstance(response, list)

    def test_get_user_contribution_calendar(self):
        response = get_user_contribution_calendar(user_id=USER_ID, access_token=TOKEN)
        self.assertIsInstance(response, RawCalendar)

    def test_get_user_contribution_events(self):
        response = get_user_contribution_events(user_id=USER_ID, access_token=TOKEN)
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
