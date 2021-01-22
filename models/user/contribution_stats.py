from enum import Enum
from typing import List

# from models.misc.date import Date
from pydantic import BaseModel, Field


"""
APIResponse
"""


class IssueEnum(str, Enum):
    """
    Enum with options OPEN, CLOSED
    """

    OPEN = "OPEN"
    CLOSED = "CLOSED"


class PREnum(str, Enum):
    """
    Enum with options OPEN, MERGED, CLOSED
    """

    OPEN = "OPEN"
    MERGED = "MERGED"
    CLOSED = "CLOSED"


class PRReviewEnum(str, Enum):
    """
    Enum with options PENDING, COMMENTED, CHANGES_REQUESTED, APPROVED, DISMISSED
    """

    PENDING = "PENDING"
    COMMENTED = "COMMENTED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    APPROVED = "APPROVED"
    DISMISSED = "DISMISSED"


class APIResponse_Repo(BaseModel):
    """
    BaseModel which accepts:
    - name: str
    """

    name: str


class APIResponse_IssueState(BaseModel):
    """
    BaseModel which accepts:
    - state: IssueEnum
    """

    state: IssueEnum


class APIResponse_PRState(BaseModel):
    """
    BaseModel which accepts:
    - state: PREnum
    """

    state: PREnum


class APIResponse_PRReviewState(BaseModel):
    """
    BaseModel which accepts:
    - state: PRReviewEnum
    """

    state: PRReviewEnum


class APIResponse_PageInfo(BaseModel):
    """
    BaseModel which accepts:
    - hasNextPage: bool
    - endCursor: str
    """

    has_next_page: bool = Field(alias="hasNextPage")
    end_cursor: str = Field(alias="endCursor")


class APIResponse_IssueContribsByRepo_Contrib(BaseModel):
    """
    BaseModel which accepts:
    - occurredAt: str
    - issue: APIResponse_State
    """

    occurred_at: str = Field(alias="occurredAt")
    issue: APIResponse_IssueState


class APIResponse_IssueContribsByRepo_Contribs(BaseModel):
    """
    BaseModel which accepts:
    - totalCount: int
    - nodes: List[APIResponse_IssueContribsByRepo_Contrib]
    - pageInfo: APIResponse_PageInfo
    """

    total_count: int = Field(alias="totalCount")
    nodes: List[APIResponse_IssueContribsByRepo_Contrib]
    page_info: APIResponse_PageInfo = Field(alias="pageInfo")


class APIResponse_IssueContribsByRepo(BaseModel):
    """
    BaseModel which accepts:
    - repository: APIResponse_Repo
    - contributions: APIResponse_IssueContribsByRepo_Contribs
    """

    repository: APIResponse_Repo
    contributions: APIResponse_IssueContribsByRepo_Contribs


class APIResponse_PRContribsByRepo_Contrib(BaseModel):
    """
    BaseModel which accepts:
    - occurredAt: str
    - pullRequest: APIResponse_State
    """

    occurred_at: str = Field(alias="occurredAt")
    pull_request: APIResponse_PRState = Field(alias="pullRequest")


class APIResponse_PRContribsByRepo_Contribs(BaseModel):
    """
    BaseModel which accepts:
    - totalCount: int
    - nodes: List[APIResponse_PRContribsByRepo_Contrib]
    - pageInfo: APIResponse_PageInfo
    """

    total_count: int = Field(alias="totalCount")
    nodes: List[APIResponse_PRContribsByRepo_Contrib]
    page_info: APIResponse_PageInfo = Field(alias="pageInfo")


class APIResponse_PRContribsByRepo(BaseModel):
    """
    BaseModel which accepts:
    - repository: APIResponse_Repo
    - contributions: APIResponse_PRContribsByRepo_Contribs
    """

    repository: APIResponse_Repo
    contributions: APIResponse_PRContribsByRepo_Contribs


class APIResponse_PRReviewContribsByRepo_Contrib(BaseModel):
    """
    BaseModel which accepts:
    - occurredAt: str
    - pullRequestReview: APIResponse_State
    """

    occurred_at: str = Field(alias="occurredAt")
    pull_request_review: APIResponse_PRReviewState = Field(alias="pullRequestReview")


class APIResponse_PRReviewContribsByRepo_Contribs(BaseModel):
    """
    BaseModel which accepts:
    - totalCount: int
    - nodes: List[APIResponse_PRReviewContribsByRepo_Contrib]
    - pageInfo: APIResponse_PageInfo
    """

    total_count: int = Field(alias="totalCount")
    nodes: List[APIResponse_PRReviewContribsByRepo_Contrib]
    page_info: APIResponse_PageInfo = Field(alias="pageInfo")


class APIResponse_PRReviewContribsByRepo(BaseModel):
    """
    BaseModel which accepts:
    - repository: APIResponse_Repo
    - contributions: APIResponse_PRReviewContribsByRepo_Contribs
    """

    repository: APIResponse_Repo
    contributions: APIResponse_PRReviewContribsByRepo_Contribs


class APIResponse_RepoContribs_Contrib(BaseModel):
    """
    BaseModel which accepts:
    - occurredAt: str
    - repository: APIResponse_Repo
    """

    occurred_at: str = Field(alias="occurredAt")
    repository: APIResponse_Repo


class APIResponse_RepoContribs(BaseModel):
    """
    BaseModel which accepts:
    - totalCount: int
    - nodes: List[APIResponse_RepoContribs_Contrib]
    - pageInfo: APIResponse_PageInfo
    """

    total_count: int = Field(alias="totalCount")
    nodes: List[APIResponse_RepoContribs_Contrib]
    page_info: APIResponse_PageInfo = Field(alias="pageInfo")


class APIResponse(BaseModel):
    """
    BaseModel which accepts:
    - issueContributionsByRepository: List[APIResponse_IssueContribsByRepo]
    - pullRequestContributionsByRepository: List[APIResponse_PRContribsByRepo]
    - pullRequestReviewContributionsByRepository: List[APIResponse_PRReviewContribsByRepo]
    - repositoryContributions: List[APIResponse_RepoContribs]
    - restrictedContributionsCount: int
    - totalIssueContributions: int
    - totalPullRequestContributions: int
    - totalPullRequestReviewContributions: int
    - totalRepositoryContributions: int
    - totalRepositoriesWithContributedIssues: int
    - totalRepositoriesWithContributedPullRequests: int
    - totalRepositoriesWithContributedPullRequestReviews: int
    """

    issue_contribs_by_repo: List[APIResponse_IssueContribsByRepo] = Field(
        alias="issueContributionsByRepository"
    )
    pr_contribs_by_repo: List[APIResponse_PRContribsByRepo] = Field(
        alias="pullRequestContributionsByRepository"
    )
    pr_review_contribs_by_repo: List[APIResponse_PRReviewContribsByRepo] = Field(
        alias="pullRequestReviewContributionsByRepository"
    )
    repo_contribs: APIResponse_RepoContribs = Field(alias="repositoryContributions")
    restricted_contrib_count: int = Field(alias="restrictedContributionsCount")
    issue_contribs_count: int = Field(alias="totalIssueContributions")
    pr_contribs_count: int = Field(alias="totalPullRequestContributions")
    pr_review_contribs_count: int = Field(alias="totalPullRequestReviewContributions")
    repo_contribs_count: int = Field(alias="totalRepositoryContributions")
    repos_with_issue_contrib: int = Field(
        alias="totalRepositoriesWithContributedIssues"
    )
    repos_with_pr_contrib: int = Field(
        alias="totalRepositoriesWithContributedPullRequests"
    )
    repos_with_pr_review_contrib: int = Field(
        alias="totalRepositoriesWithContributedPullRequestReviews"
    )
