from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel


class Language(BaseModel):
    color: Optional[str]
    additions: int
    deletions: int

    def compress(self) -> List[Any]:
        return [self.color, self.additions, self.deletions]

    @classmethod
    def decompress(cls, data: List[Any]) -> "Language":
        return Language(color=data[0], additions=data[1], deletions=data[2])

    def __add__(self, other: "Language") -> "Language":
        return Language(
            color=self.color,
            additions=self.additions + other.additions,
            deletions=self.deletions + other.deletions,
        )


class ContributionStats(BaseModel):
    contribs_count: int
    commits_count: int
    issues_count: int
    prs_count: int
    reviews_count: int
    repos_count: int
    other_count: int
    languages: Dict[str, Language]

    def compress(self) -> List[Any]:
        out: List[Any] = [
            [
                self.contribs_count,
                self.commits_count,
                self.issues_count,
                self.prs_count,
                self.reviews_count,
                self.repos_count,
                self.other_count,
            ],
            *[[name] + stats.compress() for name, stats in self.languages.items()],
        ]

        return out

    @classmethod
    def decompress(cls, data: List[Any]) -> "ContributionStats":
        return ContributionStats(
            contribs_count=data[0][0],
            commits_count=data[0][1],
            issues_count=data[0][2],
            prs_count=data[0][3],
            reviews_count=data[0][4],
            repos_count=data[0][5],
            other_count=data[0][6],
            languages={x[0]: Language.decompress(x[1:]) for x in data[1:]},
        )

    def __add__(self, other: "ContributionStats") -> "ContributionStats":
        languages = self.languages
        for lang, lang_obj in other.languages.items():
            if lang in languages:
                languages[lang] += lang_obj
            else:
                languages[lang] = lang_obj

        return ContributionStats(
            contribs_count=self.contribs_count + other.contribs_count,
            commits_count=self.commits_count + other.commits_count,
            issues_count=self.issues_count + other.issues_count,
            prs_count=self.prs_count + other.prs_count,
            reviews_count=self.reviews_count + other.reviews_count,
            repos_count=self.repos_count + other.repos_count,
            other_count=self.other_count + other.other_count,
            languages=languages,
        )

    @classmethod
    def empty(cls) -> "ContributionStats":
        return ContributionStats(
            contribs_count=0,
            commits_count=0,
            issues_count=0,
            prs_count=0,
            reviews_count=0,
            repos_count=0,
            other_count=0,
            languages={},
        )


class ContributionLists(BaseModel):
    commits: List[datetime]
    issues: List[datetime]
    prs: List[datetime]
    reviews: List[datetime]
    repos: List[datetime]

    def compress(self) -> List[Any]:
        return [self.commits, self.issues, self.prs, self.reviews, self.repos]

    @classmethod
    def decompress(cls, data: List[Any]) -> "ContributionLists":
        return ContributionLists(
            commits=data[0], issues=data[1], prs=data[2], reviews=data[3], repos=data[4]
        )


class ContributionDay(BaseModel):
    date: str
    weekday: int
    stats: ContributionStats
    lists: ContributionLists

    def compress(self) -> List[Any]:
        return [
            self.date,
            self.weekday,
            self.stats.compress(),
            self.lists.compress(),
        ]

    @classmethod
    def decompress(cls, data: List[Any]) -> "ContributionDay":
        return ContributionDay(
            date=data[0],
            weekday=data[1],
            stats=ContributionStats.decompress(data[2]),
            lists=ContributionLists.decompress(data[3]),
        )


class RepoContributionStats(ContributionStats, BaseModel):
    private: bool
    contribs_count: int
    commits_count: int
    issues_count: int
    prs_count: int
    reviews_count: int
    repos_count: int
    other_count: int
    languages: Dict[str, Language]

    def compress(self) -> List[Any]:
        out = super().compress()
        out[0].append(self.private)
        return out

    @classmethod
    def decompress(cls, data: List[Any]) -> "RepoContributionStats":
        contribs = super().decompress(data).model_dump()
        contribs["private"] = data[0][7]
        return RepoContributionStats(**contribs)

    def __add__(  # type: ignore
        self, other: "RepoContributionStats"
    ) -> "RepoContributionStats":
        new_self = ContributionStats(**self.model_dump())
        new_other = ContributionStats(**other.model_dump())
        combined = (new_self + new_other).model_dump()
        combined["private"] = self.private
        return RepoContributionStats(**combined)


class UserContributions(BaseModel):
    total_stats: ContributionStats
    public_stats: ContributionStats
    total: List[ContributionDay]
    public: List[ContributionDay]
    repo_stats: Dict[str, RepoContributionStats]
    repos: Dict[str, List[ContributionDay]]

    def compress(self) -> List[Any]:
        new_total_stats = self.total_stats.compress()
        new_public_stats = self.public_stats.compress()
        new_total = [x.compress() for x in self.total]
        new_public = [x.compress() for x in self.public]
        new_repo_stats = {k: v.compress() for k, v in self.repo_stats.items()}
        new_repos = {k: [x.compress() for x in v] for k, v in self.repos.items()}

        return [
            new_total_stats,
            new_public_stats,
            new_total,
            new_public,
            new_repo_stats,
            new_repos,
        ]

    @classmethod
    def decompress(cls, data: List[Any]) -> "UserContributions":
        total_stats = ContributionStats.decompress(data[0])
        public_stats = ContributionStats.decompress(data[1])
        total = [ContributionDay.decompress(x) for x in data[2]]
        public = [ContributionDay.decompress(x) for x in data[3]]
        repo_stats = {
            k: RepoContributionStats.decompress(v) for k, v in data[4].items()
        }
        repos = {
            k: [ContributionDay.decompress(x) for x in v] for k, v in data[5].items()
        }

        return UserContributions(
            total_stats=total_stats,
            public_stats=public_stats,
            total=total,
            public=public,
            repo_stats=repo_stats,
            repos=repos,
        )

    def __add__(self, other: "UserContributions") -> "UserContributions":
        new_total_stats = self.total_stats + other.total_stats
        new_public_stats = self.public_stats + other.public_stats
        new_total = sorted(self.total + other.total, key=lambda x: x.date)
        new_public = sorted(self.public + other.public, key=lambda x: x.date)
        new_repo_stats = self.repo_stats
        for repo, stats in other.repo_stats.items():
            if repo in new_repo_stats:
                new_repo_stats[repo] += stats
            else:
                new_repo_stats[repo] = stats
        new_repos = self.repos
        for repo, days in other.repos.items():
            if repo in new_repos:
                new_repos[repo] = sorted(new_repos[repo] + days, key=lambda x: x.date)
            else:
                new_repos[repo] = days

        return UserContributions(
            total_stats=new_total_stats,
            public_stats=new_public_stats,
            total=new_total,
            public=new_public,
            repo_stats=new_repo_stats,
            repos=new_repos,
        )

    @staticmethod
    def trim_contribs(
        contribs: List[ContributionDay], start_date: date, end_date: date
    ) -> Tuple[List[ContributionDay], ContributionStats]:
        new_total: List[ContributionDay] = []
        for day in contribs:
            curr_date = datetime.strptime(day.date, "%Y-%m-%d").date()
            if curr_date >= start_date and curr_date <= end_date:
                new_total.append(day)

        new_languages: Dict[str, Language] = {}
        for day in new_total:
            for lang in day.stats.languages:
                if lang in new_languages:
                    new_languages[lang] += day.stats.languages[lang]
                else:
                    new_languages[lang] = day.stats.languages[lang]

        new_stats = ContributionStats(
            contribs_count=sum(x.stats.contribs_count for x in new_total),
            commits_count=sum(x.stats.commits_count for x in new_total),
            issues_count=sum(x.stats.issues_count for x in new_total),
            prs_count=sum(x.stats.prs_count for x in new_total),
            reviews_count=sum(x.stats.reviews_count for x in new_total),
            repos_count=sum(x.stats.repos_count for x in new_total),
            other_count=sum(x.stats.other_count for x in new_total),
            languages=new_languages,
        )

        return new_total, new_stats

    def trim(self, start: date, end: date) -> "UserContributions":
        new_total, new_total_stats = self.trim_contribs(self.total, start, end)
        new_public, new_public_stats = self.trim_contribs(self.public, start, end)

        new_repos_dict: Dict[str, List[ContributionDay]] = {}
        new_repo_stats_dict: Dict[str, RepoContributionStats] = {}
        for repo_name, repo in self.repos.items():
            new_repo_total, _new_repo_stats = self.trim_contribs(repo, start, end)
            if len(new_repo_total) > 0:
                new_repos_dict[repo_name] = new_repo_total
                raw_new_repo_stats = _new_repo_stats.model_dump()
                raw_new_repo_stats["private"] = self.repo_stats[repo_name].private
                new_repo_stats = RepoContributionStats(**raw_new_repo_stats)
                new_repo_stats_dict[repo_name] = new_repo_stats

        return UserContributions(
            total_stats=new_total_stats,
            public_stats=new_public_stats,
            total=new_total,
            public=new_public,
            repo_stats=new_repo_stats_dict,
            repos=new_repos_dict,
        )

    @classmethod
    def empty(cls) -> "UserContributions":
        return UserContributions(
            total_stats=ContributionStats.empty(),
            public_stats=ContributionStats.empty(),
            total=[],
            public=[],
            repo_stats={},
            repos={},
        )
