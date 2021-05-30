from typing import Any, Dict, List, Union

from models.user.package import UserPackage

dict_type = Dict[str, Union[str, int, float]]


def get_top_languages(data: UserPackage) -> List[dict_type]:
    raw_languages = data.contribs.total_stats.languages
    languages_list: List[dict_type] = [
        {
            "lang": lang,
            "additions": stats.additions,
            "deletions": stats.deletions,
        }
        for lang, stats in raw_languages.items()
    ]

    total_additions = sum([int(lang["additions"]) for lang in languages_list])
    total_deletions = sum([int(lang["deletions"]) for lang in languages_list])
    total_changed = total_additions + total_deletions
    total: dict_type = {
        "lang": "Total",
        "additions": total_additions,
        "deletions": total_deletions,
    }

    languages_list = sorted(
        languages_list,
        key=lambda x: int(x["additions"]) + int(x["deletions"]),
        reverse=True,
    )
    other: dict_type = {"lang": "Other", "additions": 0, "deletions": 0}
    for language in languages_list[5:]:
        other["additions"] = int(other["additions"]) + int(language["additions"])
        other["deletions"] = int(other["deletions"]) + int(language["deletions"])

    languages_list = [total] + languages_list[:5] + [other]

    for lang in languages_list:
        lang["added"] = int(lang["additions"]) - int(lang["deletions"])
        lang["changed"] = int(lang["additions"]) + int(lang["deletions"])
        lang["percent"] = float(round(100 * lang["changed"] / total_changed, 2))

    return languages_list


def get_top_repos(data: UserPackage) -> List[Any]:
    repos: List[Any] = [
        {
            repo: repo,
            "languages": [lang for lang in repo_stats.languages],
            "additions": sum([x.additions for x in repo_stats.languages.values()]),
            "deletions": sum([x.deletions for x in repo_stats.languages.values()]),
        }
        for repo, repo_stats in data.contribs.repo_stats.items()
    ]

    for repo in repos:
        repo["added"] = int(repo["additions"]) - int(repo["deletions"])
        repo["changed"] = int(repo["additions"]) + int(repo["deletions"])

    repos = sorted(repos, key=lambda x: x["changed"], reverse=True)

    return repos[:5]
