from typing import List, Optional

from pydantic import BaseModel


class LanguageStats(BaseModel):
    lang: str
    additions: int
    deletions: int
    added: int
    changed: int
    percent: float
    color: Optional[str]


class RepoLanguage(BaseModel):
    lang: str
    color: str
    additions: int
    deletions: int


class RepoStats(BaseModel):
    repo: str
    private: bool
    langs: List[RepoLanguage]
    additions: int
    deletions: int
    added: int
    changed: int
