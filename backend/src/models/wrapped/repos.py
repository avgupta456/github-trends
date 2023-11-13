from typing import List

from pydantic import BaseModel


class RepoDatum(BaseModel):
    id: int
    label: str
    value: int
    formatted_value: str


class RepoData(BaseModel):
    repos_changed: List[RepoDatum]
    repos_added: List[RepoDatum]

    @classmethod
    def empty(cls) -> "RepoData":
        return RepoData(repos_changed=[], repos_added=[])
