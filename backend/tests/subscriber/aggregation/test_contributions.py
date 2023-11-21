from datetime import date, timedelta

from aiounittest.case import AsyncTestCase

from src.constants import TEST_TOKEN as TOKEN, TEST_USER_ID as USER_ID
from src.models import UserContributions
from src.processing.layer0 import get_contributions


class TestTemplate(AsyncTestCase):
    async def test_get_contributions(self):
        response = await get_contributions(
            user_id=USER_ID,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today(),
            access_token=TOKEN,
        )
        self.assertIsInstance(response, UserContributions)

        # TODO: Add further validation
