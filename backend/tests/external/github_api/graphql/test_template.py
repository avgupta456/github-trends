import unittest

from external.github_api.graphql.template import get_template
from constants import TOKEN


class TestTemplate(unittest.TestCase):
    def test_get_template(self):
        query = {
            "variables": {"login": "avgupta456"},
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
