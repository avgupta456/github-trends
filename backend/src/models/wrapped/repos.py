from typing import List

from pydantic import BaseModel


class RepoDatum(BaseModel):
    id: str
    label: str
    value: int
    formatted_value: str


class RepoData(BaseModel):
    repos_changed: List[RepoDatum]
    repos_added: List[RepoDatum]
