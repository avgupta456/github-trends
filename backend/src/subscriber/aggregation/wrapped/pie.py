from typing import List

from src.models import (
    FullUserPackage,
    RepoContributionStats,
    Language,
    PieData,
    PieDatum,
)
from src.utils import format_number


def _loc_changed(x: Language) -> int:
    return x.additions + x.deletions


def _count_repo_loc_changed(x: RepoContributionStats) -> int:
    return sum(_loc_changed(lang) for lang in x.languages.values())


def get_pie_data(data: FullUserPackage) -> PieData:
    # REPO PIE CHART
    stores = [
        data.contribs.repo_stats.items(),
        [(k, v) for k, v in data.contribs.repo_stats.items() if not v.private],
    ]
    out = {}
    for key, store in zip(["repos", "public_repos"], stores):
        repos = sorted(store, key=lambda x: _count_repo_loc_changed(x[1]), reverse=True)
        repo_objs: List[PieDatum] = []
        for k, v in list(repos)[:5]:
            repo_data = {
                "id": k,
                "label": "private/repository" if v.private else k,
                "value": _count_repo_loc_changed(v),
                "formatted_value": format_number(_count_repo_loc_changed(v)),
            }
            repo_objs.append(PieDatum.parse_obj(repo_data))
        out[key] = repo_objs

    # LANGUAGE PIE CHART
    stores = [
        data.contribs.total_stats.languages.items(),
        data.contribs.public_stats.languages.items(),
    ]
    for key, store in zip(["langs", "public_langs"], stores):
        langs = sorted(store, key=lambda x: _loc_changed(x[1]), reverse=True)
        lang_objs: List[PieDatum] = []
        for k, v in list(langs)[:5]:
            lang_data = {
                "id": k,
                "label": k,
                "value": _loc_changed(v),
                "formatted_value": format_number(_loc_changed(v)),
                "color": v.color,
            }
            lang_objs.append(PieDatum.parse_obj(lang_data))
        out[key] = lang_objs

    return PieData.parse_obj(out)
