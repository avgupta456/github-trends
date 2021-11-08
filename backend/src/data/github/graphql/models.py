from typing import List
from pydantic import BaseModel, Field


class RawCommit(BaseModel):
    additions: int
    deletions: int
    changed_files: int = Field(alias="changedFiles")


class RawRepoLanguageNode(BaseModel):
    name: str
    color: str


class RawRepoLanguageEdge(BaseModel):
    node: RawRepoLanguageNode
    size: int


class RawRepoLanguage(BaseModel):
    total_count: int = Field(alias="totalCount")
    total_size: int = Field(alias="totalSize")
    edges: List[RawRepoLanguageEdge]


class RawRepo(BaseModel):
    is_private: bool = Field(alias="isPrivate")
    fork_count: int = Field(alias="forkCount")
    stargazer_count: int = Field(alias="stargazerCount")
    languages: RawRepoLanguage
