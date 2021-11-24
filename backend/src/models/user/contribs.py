from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class CommitContribution(BaseModel):
    timestamp: str
    languages: Dict[str, Dict[str, Union[int, str]]]


class Language(BaseModel):
    color: Optional[str]
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

    # temporarily remove list from total to reduce storage
    # TODO: improve compression so this is not necessary
    # lists: ContributionLists


class FullContributionDay(BaseModel):
    date: str
    weekday: int
    stats: ContributionStats
    lists: ContributionLists


class RepoContributionStats(BaseModel):
    private: bool
    contribs_count: int
    commits_count: int
    issues_count: int
    prs_count: int
    reviews_count: int
    repos_count: int
    other_count: int
    languages: Dict[str, Language]


class UserContributions(BaseModel):
    total_stats: ContributionStats
    public_stats: ContributionStats
    total: List[ContributionDay]
    public: List[ContributionDay]
    repo_stats: Dict[str, RepoContributionStats]
    repos: Dict[str, List[ContributionDay]]


class FullUserContributions(BaseModel):
    total_stats: ContributionStats
    public_stats: ContributionStats
    total: List[FullContributionDay]
    public: List[FullContributionDay]
    repo_stats: Dict[str, RepoContributionStats]
    repos: Dict[str, List[FullContributionDay]]
