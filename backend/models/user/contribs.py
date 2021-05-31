from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class RawCalendarDay(BaseModel):
    date: date
    weekday: int
    count: int = Field(alias="contributionCount")


class RawCalendarWeek(BaseModel):
    contribution_days: List[RawCalendarDay] = Field(alias="contributionDays")


class RawCalendar(BaseModel):
    total_contributions: int = Field(alias="totalContributions")
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


class CommitContribution(BaseModel):
    timestamp: str
    languages: Dict[str, Dict[str, int]]


class Language(BaseModel):
    additions: int
    deletions: int


class ContributionStats(BaseModel):
    contribs_count: int
    commits_count: int
    issues_count: int
    prs_count: int
    reviews_count: int
    repos_count: int
    other_count: int
    languages: Dict[str, Language]


class ContributionLists(BaseModel):
    commits: List[CommitContribution]
    issues: List[str]
    prs: List[str]
    reviews: List[str]
    repos: List[str]


class ContributionDay(BaseModel):
    date: str
    weekday: int
    stats: ContributionStats
    lists: ContributionLists


class UserContributions(BaseModel):
    total_stats: ContributionStats
    total: List[ContributionDay]
    repo_stats: Dict[str, ContributionStats]
    repos: Dict[str, List[ContributionDay]]
