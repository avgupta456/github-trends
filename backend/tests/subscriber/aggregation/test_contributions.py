from aiounittest.case import AsyncTestCase

from src.models import UserContributions

from src.subscriber.aggregation import get_contributions

from src.constants import TEST_USER_ID as USER_ID, TEST_TOKEN as TOKEN


class TestTemplate(AsyncTestCase):
    async def test_get_contributions(self):
        response = await get_contributions(USER_ID, TOKEN)
        self.assertIsInstance(response, UserContributions)

        # TODO: Add further validation
