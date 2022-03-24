from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class RawCalendarDay(BaseModel):
    date: date
    weekday: int
    count: int = Field(alias="contributionCount")


class RawCalendarWeek(BaseModel):
    contribution_days: List[RawCalendarDay] = Field(alias="contributionDays")


class RawCalendar(BaseModel):
    weeks: List[RawCalendarWeek]


class RawEventsRepoName(BaseModel):
    name: str = Field(alias="nameWithOwner")


class RawEventsCount(BaseModel):
    count: int = Field(alias="totalCount")


class RawEventsCommit(BaseModel):
    count: int = Field(alias="commitCount")
    occurred_at: datetime = Field(alias="occurredAt")


class RawEventsEvent(BaseModel):
    occurred_at: datetime = Field(alias="occurredAt")


class RawEventsPageInfo(BaseModel):
    has_next_page: bool = Field(alias="hasNextPage")
    end_cursor: Optional[str] = Field(alias="endCursor")

    class Config:
        allow_none = True


class RawEventsCommits(BaseModel):
    nodes: List[RawEventsCommit]
    page_info: RawEventsPageInfo = Field(alias="pageInfo")


class RawEventsContribs(BaseModel):
    nodes: List[RawEventsEvent]
    page_info: RawEventsPageInfo = Field(alias="pageInfo")


class RawEventsRepoCommits(BaseModel):
    repo: RawEventsRepoName = Field(alias="repository")
    count: RawEventsCount = Field(alias="totalCount")
    contribs: RawEventsCommits = Field(alias="contributions")


class RawEventsRepo(BaseModel):
    repo: RawEventsRepoName = Field(alias="repository")
    count: RawEventsCount = Field(alias="totalCount")
    contribs: RawEventsContribs = Field(alias="contributions")


class RawEventsRepoEvent(BaseModel):
    repo: RawEventsRepoName = Field(alias="repository")
    occurred_at: datetime = Field(alias="occurredAt")


class RawEventsRepoContribs(BaseModel):
    count: int = Field(alias="totalCount")
    nodes: List[RawEventsRepoEvent]


class RawEvents(BaseModel):
    commit_contribs_by_repo: List[RawEventsRepoCommits] = Field(
        alias="commitContributionsByRepository"
    )
    issue_contribs_by_repo: List[RawEventsRepo] = Field(
        alias="issueContributionsByRepository"
    )
    pr_contribs_by_repo: List[RawEventsRepo] = Field(
        alias="pullRequestContributionsByRepository"
    )
    review_contribs_by_repo: List[RawEventsRepo] = Field(
        alias="pullRequestReviewContributionsByRepository"
    )
    repo_contribs: RawEventsRepoContribs = Field(alias="repositoryContributions")
