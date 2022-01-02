from typing import Any, Dict, List, Tuple, Union

from src.constants import DEFAULT_COLOR
from src.models import UserPackage
from src.publisher.aggregation.user.models import LanguageStats, RepoStats

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

    languages_list: List[dict_type] = [
        {
            "lang": lang,
            "color": stats.color or DEFAULT_COLOR,
            "loc": loc_metric_func(loc_metric, stats.additions, stats.deletions),
        }
        for lang, stats in raw_languages.items()
    ]

    languages_list = list(filter(lambda x: x["loc"] > 0, languages_list))  # type: ignore

    total_loc: int = sum(x["loc"] for x in languages_list) + 1  # type: ignore
    total: dict_type = {"lang": "Total", "loc": total_loc}

    languages_list = sorted(languages_list, key=lambda x: x["loc"], reverse=True)
    other: dict_type = {"lang": "Other", "loc": 0, "color": "#ededed"}
    for language in languages_list[4:]:
        other["loc"] = int(other["loc"]) + int(language["loc"])

    languages_list = [total] + languages_list[:4] + [other]

    new_languages_list: List[LanguageStats] = []
    for lang in languages_list:
        lang["percent"] = float(round(100 * int(lang["loc"]) / total_loc, 2))
        if lang["percent"] > 1:  # 1% minimum to show
            new_languages_list.append(LanguageStats.parse_obj(lang))

    commits_excluded = data.contribs.public_stats.other_count
    if include_private:
        commits_excluded = data.contribs.total_stats.other_count

    return new_languages_list, commits_excluded


def get_top_repos(
    data: UserPackage, loc_metric: str, include_private: bool
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
        RepoStats.parse_obj(x) for x in repos if x["loc"] > 0.01 * repos[0]["loc"]
    ]

    commits_excluded = data.contribs.public_stats.other_count
    if include_private:
        commits_excluded = data.contribs.total_stats.other_count

    return new_repos[:5], commits_excluded
