from models.misc.date import Date
from typing import List, Optional

# from models.misc.date import Date
from pydantic import BaseModel, Field


"""
APIResponse
"""


class APIResponse_Repo(BaseModel):
    """
    BaseModel which accepts:
    - name: str
    """

    name: str


class APIResponse_PageInfo(BaseModel):
    """
    BaseModel which accepts:
    - hasNextPage: bool
    - endCursor: str
    """

    has_next_page: bool = Field(alias="hasNextPage")
    end_cursor: Optional[str] = Field(alias="endCursor")

    class Config:
        allow_none = True


class APIResponse_Contrib(BaseModel):
    """
    BaseModel which accepts:
    - occurredAt: str
    """

    occurred_at: str = Field(alias="occurredAt")


class APIResponse_Contribs(BaseModel):
    """
    BaseModel which accepts:
    - totalCount: int
    - nodes: List[APIResponse_Contrib]
    - pageInfo: APIResponse_PageInfo
    """

    total_count: int = Field(alias="totalCount")
    nodes: List[APIResponse_Contrib]
    page_info: APIResponse_PageInfo = Field(alias="pageInfo")


class APIResponse_ContribsByRepo(BaseModel):
    """
    BaseModel which accepts:
    - repository: APIResponse_Repo
    - contributions: APIResponse_Contribs
    """

    repository: APIResponse_Repo
    contributions: APIResponse_Contribs


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
    - issueContributionsByRepository: List[APIResponse_ContribsByRepo]
    - pullRequestContributionsByRepository: List[APIResponse_ContribsByRepo]
    - pullRequestReviewContributionsByRepository: List[APIResponse_ContribsByRepo]
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

    issue_contribs_by_repo: List[APIResponse_ContribsByRepo] = Field(
        alias="issueContributionsByRepository"
    )
    pr_contribs_by_repo: List[APIResponse_ContribsByRepo] = Field(
        alias="pullRequestContributionsByRepository"
    )
    pr_review_contribs_by_repo: List[APIResponse_ContribsByRepo] = Field(
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


"""
EXTERNAL
"""


class Contribution(BaseModel):
    """
    BaseModel which accepts:
    - occurred_at: Date
    """

    occurred_at: Date

    class Config:
        arbitrary_types_allowed = True


class RepoContribStats(BaseModel):
    """
    BaseModel which includes:
    - name: str
    - issues: List[Contribution]
    - prs: List[Contribution]
    - reviews: List[Contribution]
    - repo: List[Contribution]
    """

    name: str
    issues: List[Contribution]
    prs: List[Contribution]
    reviews: List[Contribution]
    repo: List[Contribution]


class ContribStats(BaseModel):
    """
    BaseModel which accepts:
    - repos: List[RepoContribStats]
    - total: RepoContribStats
    - restricted_contrib_count: int
    - issue_contribs_count: int
    - pr_contribs_count: int
    - pr_review_contribs_count: int
    - repo_contribs_count: int
    - repos_with_issue_contrib: int
    - repos_with_pr_contrib: int
    - repos_with_pr_review_contrib: int
    """

    repos: List[RepoContribStats]
    total: RepoContribStats

    restricted_contrib_count: int
    issue_contribs_count: int
    pr_contribs_count: int
    pr_review_contribs_count: int
    repo_contribs_count: int
    repos_with_issue_contrib: int
    repos_with_pr_contrib: int
    repos_with_pr_review_contrib: int
