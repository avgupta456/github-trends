from typing import Any, Dict, List, Optional, Tuple, Union

from src.constants import DEFAULT_COLOR
from src.models import UserPackage
from src.models.svg import LanguageStats, RepoStats

dict_type = Dict[str, Union[str, int, float]]


def loc_metric_func(loc_metric: str, additions: int, deletions: int) -> int:
    if loc_metric == "changed":
        return additions + deletions
    return additions - deletions


def get_top_languages(
    data: UserPackage, loc_metric: str, include_private: bool
) -> Tuple[List[LanguageStats], int]:
    raw_languages = (
        data.contribs.total_stats.languages
        if include_private
        else data.contribs.public_stats.languages
    )

    languages_list = [
        LanguageStats(
            lang=lang,
            color=stats.color or DEFAULT_COLOR,
            loc=loc_metric_func(loc_metric, stats.additions, stats.deletions),
            percent=-1,
        )
        for lang, stats in raw_languages.items()
    ]

    languages_list = list(filter(lambda x: x.loc > 0, languages_list))

    total_loc = sum(x.loc for x in languages_list) + 1
    total = LanguageStats(lang="Total", color=None, loc=total_loc, percent=100)

    languages_list = sorted(languages_list, key=lambda x: x.loc, reverse=True)
    other = LanguageStats(lang="Other", color="#ededed", loc=0, percent=-1)
    for language in languages_list[4:]:
        other.loc = other.loc + language.loc

    languages_list = [total] + languages_list[:4] + [other]

    new_languages_list: List[LanguageStats] = []
    for lang in languages_list:
        lang.percent = float(round(100 * lang.loc / total_loc, 2))
        if lang.percent > 1:  # 1% minimum to show
            new_languages_list.append(LanguageStats.model_validate(lang))

    commits_excluded = data.contribs.public_stats.other_count
    if include_private:
        commits_excluded = data.contribs.total_stats.other_count

    return new_languages_list, commits_excluded


def get_top_repos(
    data: UserPackage, loc_metric: str, include_private: bool, group: str
) -> Tuple[List[RepoStats], int]:
    repos: List[Any] = [
        {
            "repo": repo,
            "private": repo_stats.private,
            "langs": [
                {
                    "lang": x[0],
                    "color": x[1].color,
                    "loc": loc_metric_func(loc_metric, x[1].additions, x[1].deletions),
                }
                for x in list(repo_stats.languages.items())
            ],
        }
        for repo, repo_stats in data.contribs.repo_stats.items()
        if include_private or not repo_stats.private
    ]

    for repo in repos:
        repo["loc"] = sum(x["loc"] for x in repo["langs"])  # first estimate
    repos = list(filter(lambda x: x["loc"] > 0, repos))

    for repo in repos:
        repo["langs"] = [x for x in repo["langs"] if x["loc"] > 0.05 * repo["loc"]]
        repo["loc"] = sum(x["loc"] for x in repo["langs"])  # final estimate
    repos = sorted(repos, key=lambda x: x["loc"], reverse=True)

    new_repos = [
        RepoStats.model_validate(x) for x in repos if x["loc"] > 0.01 * repos[0]["loc"]
    ]

    commits_excluded = data.contribs.public_stats.other_count
    if include_private:
        commits_excluded = data.contribs.total_stats.other_count

    # With n bars, group from n onwards into the last bar
    bars = 4  # TODO: make this configurable (see issues)

    if group == "none" or len(new_repos) <= bars:
        return new_repos[:bars], commits_excluded

    out_repos = []
    other_repos = []
    if group == "other":
        out_repos = new_repos[: bars - 1]
        other_repos = new_repos[bars - 1 :]
    elif group == "private":
        public_repos = [x for x in new_repos if not x.private]
        private_repos = [x for x in new_repos if x.private]
        if len(public_repos) < 4 and len(private_repos) > 0:
            public_repos += private_repos[: bars - len(public_repos) - 1]
            private_repos = private_repos[bars - len(public_repos) - 1 :]
        out_repos = sorted(public_repos[: bars - 1], key=lambda x: x.loc, reverse=True)
        other_repos = public_repos[bars - 1 :] + private_repos
    else:
        raise ValueError("Invalid group value")

    other: Dict[str, Tuple[int, Optional[str]]] = {}
    for repo in other_repos:
        for _lang in repo.langs:
            lang = _lang.lang
            if lang not in other:
                other[lang] = (0, _lang.color)
            other[lang] = (other[lang][0] + _lang.loc, other[lang][1])

    out_repos.append(
        RepoStats(
            repo="other/repos",
            private=False,
            langs=[{"lang": k, "loc": v[0], "color": v[1]} for k, v in other.items()],  # type: ignore
            loc=sum(v[0] for v in other.values()),
        )
    )

    return out_repos, commits_excluded
