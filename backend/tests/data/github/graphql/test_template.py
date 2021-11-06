import unittest

from src.data.github.graphql.template import get_template
from src.constants import TEST_USER_ID as USER_ID, TEST_TOKEN as TOKEN


class TestTemplate(unittest.TestCase):
    def test_get_template(self):
        query = {
            "variables": {"login": USER_ID},
            "query": """
            query getUser($login: String!) {
                user(login: $login){
                    contributionsCollection{
                        contributionCalendar{
                            totalContributions
                        }
                    }
                }
            }
            """,
        }
        response = get_template(query, TOKEN)

        self.assertIn("data", response)
        data = response["data"]
        self.assertIn("user", data)
        user = data["user"]
        self.assertIn("contributionsCollection", user)
        contributionsCollection = user["contributionsCollection"]
        self.assertIn("contributionCalendar", contributionsCollection)
        contributionCalendar = contributionsCollection["contributionCalendar"]
        self.assertIn("totalContributions", contributionCalendar)
        totalContributions = contributionCalendar["totalContributions"]
        self.assertGreater(totalContributions, 0)
