import aiounittest

from models.user.contribs import UserContributions

from processing.user.contributions import get_contributions

from constants import TEST_USER_ID as USER_ID, TOKEN


class TestTemplate(aiounittest.AsyncTestCase):
    async def test_get_contributions(self):
        response = await get_contributions(USER_ID, TOKEN)
        self.assertIsInstance(response, UserContributions)

        # TODO: Add further validation
