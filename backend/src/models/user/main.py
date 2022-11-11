from datetime import date
from typing import Any, Dict

from pydantic import BaseModel

from src.models.user.contribs import UserContributions

# from src.models.user.follows import UserFollows


class UserPackage(BaseModel):
    contribs: UserContributions
    incomplete: bool = False

    def compress(self):
        return {
            "c": self.contribs.compress(),
        }

    @classmethod
    def decompress(cls, data: Dict[str, Any]) -> "UserPackage":
        return UserPackage(
            contribs=UserContributions.decompress(data["c"]),
        )

    def __add__(self, other: "UserPackage") -> "UserPackage":
        return UserPackage(contribs=self.contribs + other.contribs)

    def trim(self, start: date, end: date) -> "UserPackage":
        return UserPackage(contribs=self.contribs.trim(start, end))

    @classmethod
    def empty(cls) -> "UserPackage":
        return UserPackage(contribs=UserContributions.empty())
