from typing import List, Optional

from pydantic import BaseModel


class LanguageStats(BaseModel):
    lang: str
    loc: int
    percent: float
    color: Optional[str]


class RepoLanguage(BaseModel):
    lang: str
    color: Optional[str]
    loc: int


class RepoStats(BaseModel):
    repo: str
    private: bool
    langs: List[RepoLanguage]
    loc: int
