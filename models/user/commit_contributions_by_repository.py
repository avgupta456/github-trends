from typing import List

from models.misc.date import Date
from pydantic import BaseModel, Field


"""
APIResponse
"""


class APIResponse_Repo_Repo(BaseModel):
    """
    BaseModel which accepts:
    - name: str
    """

    name: str


class APIResponse_Repo_TotalCount(BaseModel):
    """
    BaseModel which accepts:
    - totalCount: int
    """

    total_count: int = Field(alias="totalCount")


class APIResponse_Repo_Contribs_Node(BaseModel):
    """
    BaseModel which accepts:
    - commitCount: int
    - occurredAt: str
    """

    commit_count: int = Field(alias="commitCount")
    occurred_at: str = Field(alias="occurredAt")


class APIResponse_Repo_Contribs_PageInfo(BaseModel):
    """
    BaseModel which accepts:
    - hasNextPage: bool
    - endCursor: str
    """

    has_next_page: bool = Field(alias="hasNextPage")
    end_cursor: str = Field(alias="endCursor")


class APIResponse_Repo_Contribs(BaseModel):
    """
    BaseModel which accepts:
    - nodes: List[APIResponse_Repo_Contribs_Nodes]
    - pageInfo: APIResponse_Repo_Contribs_PageInfo
    """

    nodes: List[APIResponse_Repo_Contribs_Node]
    page_info: APIResponse_Repo_Contribs_PageInfo = Field(alias="pageInfo")


class APIResponse_Repo(BaseModel):
    """
    BaseModel which accepts:
    - repository: APIResponse_Repo_Repo
    - totalCount: APIResponse_Repo_TotalCount
    - contributions: APIResponse_Repo_Contribs
    """

    repository: APIResponse_Repo_Repo
    total_count: APIResponse_Repo_TotalCount = Field(alias="totalCount")
    contributions: APIResponse_Repo_Contribs


class APIResponse(BaseModel):
    """
    BaseModel which accepts:
    - data: List[APIResponse_Repo]
    """

    data: List[APIResponse_Repo]


"""
EXTERNAL
"""


class CommitContribution(BaseModel):
    """
    BaseModel which accepts:
    - commitCount: int
    - occuredAt: str
    """

    commit_count: int
    occurred_at: Date

    class Config:
        arbitrary_types_allowed = True


def create_commit_contribution(x: APIResponse_Repo_Contribs_Node) -> CommitContribution:
    """helper function to create a CommitContribution"""
    return CommitContribution(
        commit_count=x.commit_count, occured_at=Date(x.occurred_at)
    )


class CommitContributionsByRepository(BaseModel):
    """
    BaseModel which accepts
    - name: str
    - contributions: int
    - contributions_in_range: int
    - timeline: List[CommitContribution]
    """

    name: str
    contributions: int
    contributions_in_range: int
    timeline: List[CommitContribution]
