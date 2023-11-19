from typing import List

from src.models import Language, RepoContributionStats, RepoData, RepoDatum, UserPackage
from src.utils import format_number


def _count_loc(x: Language, metric: str) -> int:
    if metric == "changed":
        return x.additions + x.deletions
    return x.additions - x.deletions


def _count_repo_loc(x: RepoContributionStats, metric: str) -> int:
    return sum(_count_loc(lang, metric) for lang in x.languages.values())


def get_repo_data(data: UserPackage) -> RepoData:
    out = {}
    for m in ["changed", "added"]:
        repos = sorted(
            data.contribs.repo_stats.items(),
            key=lambda x: _count_repo_loc(x[1], m),
            reverse=True,
        )
        repo_objs: List[RepoDatum] = []

        # first five repositories
        for i, (k, v) in enumerate(list(repos)[:5]):
            repo_data = {
                "id": i,
                "label": "private/repository" if v.private else k,
                "value": _count_repo_loc(v, m),
                "formatted_value": format_number(_count_repo_loc(v, m)),
            }
            repo_objs.append(RepoDatum.model_validate(repo_data))

        # remaining repositories
        total_count = sum(_count_repo_loc(v, m) for _, v in list(repos)[5:])
        repo_data = {
            "id": -1,
            "label": "other",
            "value": total_count,
            "formatted_value": format_number(total_count),
        }
        if total_count > 100:
            repo_objs.append(RepoDatum.model_validate(repo_data))

        out[f"repos_{m}"] = repo_objs

    return RepoData.model_validate(out)
