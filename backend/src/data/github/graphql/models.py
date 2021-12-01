from typing import List, Optional

from pydantic import BaseModel, Field


class RawCommitPRFileNode(BaseModel):
    path: str
    additions: int
    deletions: int


class RawCommitPRFile(BaseModel):
    nodes: List[RawCommitPRFileNode]


class RawCommitPRNode(BaseModel):
    changed_files: int = Field(alias="changedFiles")
    additions: int
    deletions: int
    files: RawCommitPRFile


class RawCommitPR(BaseModel):
    nodes: List[RawCommitPRNode]


class RawCommit(BaseModel):
    additions: int
    deletions: int
    changed_files: int = Field(alias="changedFiles")
    url: str
    prs: RawCommitPR = Field(alias="associatedPullRequests")


class RawRepoLanguageNode(BaseModel):
    name: str
    color: Optional[str]


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
