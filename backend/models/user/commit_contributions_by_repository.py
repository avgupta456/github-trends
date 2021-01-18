# type: ignore

from typing import List

from pydantic import BaseModel, Field


class CommitContribution(BaseModel):
    """
    BaseModel which accepts:
    - commitCount: int
    - occuredAt: str
    """

    commit_count: int = Field(alias="commitCount")
    occurred_at: str = Field(alias="occurredAt")


class CommitContributionsByRepository(BaseModel):
    """
    BaseModel which accepts
    - name: str
    - contributions: int
    - timeline: List[CommitContribution]
    """

    name: str
    contributions: int
    timeline: List[CommitContribution]