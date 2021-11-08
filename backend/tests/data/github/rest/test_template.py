from typing import Any, List
import unittest

from src.data.github.rest.template import get_template
from src.constants import (
    TEST_USER_ID as USER_ID,
    TEST_TOKEN as TOKEN,
    TEST_REPO as REPO,
)


class TestTemplate(unittest.TestCase):
    def test_get_template(self):
        BASE_URL = "https://api.github.com/repos/"
        query = BASE_URL + USER_ID + "/" + REPO + "/stats/contributors"
        response: List[Any] = get_template(query, TOKEN)  # type: ignore

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
