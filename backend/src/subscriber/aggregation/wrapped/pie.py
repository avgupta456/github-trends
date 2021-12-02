from typing import List

from src.constants import DEFAULT_COLOR
from src.models import (
    FullUserPackage,
    Language,
    PieData,
    PieDatum,
    RepoContributionStats,
)
from src.utils import format_number


def _count_loc(x: Language, metric: str) -> int:
    if metric == "changed":
        return x.additions + x.deletions
    return x.additions - x.deletions


def _count_repo_loc(x: RepoContributionStats, metric: str) -> int:
    return sum(_count_loc(lang, metric) for lang in x.languages.values())


def get_pie_data(data: FullUserPackage) -> PieData:
    # REPO PIE CHART
    out = {}
    for m in ["changed", "added"]:
        repos = sorted(
            data.contribs.repo_stats.items(),
            key=lambda x: _count_repo_loc(x[1], m),
            reverse=True,
        )
        repo_objs: List[PieDatum] = []

        # first five repositories
        for i, (k, v) in enumerate(list(repos)[:5]):
            repo_data = {
                "id": i,
                "label": "private/repository" if v.private else k,
                "value": _count_repo_loc(v, m),
                "formatted_value": format_number(_count_repo_loc(v, m)),
            }
            repo_objs.append(PieDatum.parse_obj(repo_data))

        # remaining repositories
        total_count = 0
        for (k, v) in list(repos)[5:]:
            total_count += _count_repo_loc(v, m)
        repo_data = {
            "id": -1,
            "label": "other",
            "value": total_count,
            "formatted_value": format_number(total_count),
        }
        if total_count > 100:
            repo_objs.append(PieDatum.parse_obj(repo_data))

        out["repos_" + m] = repo_objs

    # LANGUAGE PIE CHART
    for m in ["changed", "added"]:
        langs = sorted(
            data.contribs.total_stats.languages.items(),
            key=lambda x: _count_loc(x[1], m),
            reverse=True,
        )
        lang_objs: List[PieDatum] = []
        for k, v in list(langs)[:5]:
            lang_data = {
                "id": k,
                "label": k,
                "value": _count_loc(v, m),
                "formatted_value": format_number(_count_loc(v, m)),
                "color": v.color,
            }
            lang_objs.append(PieDatum.parse_obj(lang_data))

        # remaining languages
        total_count = 0
        for (k, v) in list(langs)[5:]:
            total_count += _count_loc(v, m)
        lang_data = {
            "id": -1,
            "label": "other",
            "value": total_count,
            "formatted_value": format_number(total_count),
            "color": DEFAULT_COLOR,
        }
        if total_count > 100:
            lang_objs.append(PieDatum.parse_obj(lang_data))

        out["langs_" + m] = lang_objs

    return PieData.parse_obj(out)
