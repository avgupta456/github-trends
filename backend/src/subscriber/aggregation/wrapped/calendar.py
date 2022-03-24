from typing import Any, Dict, List

from src.models import CalendarDayData, UserPackage


def get_calendar_data(data: UserPackage) -> List[CalendarDayData]:
    top_langs = [
        x[0]
        for x in sorted(
            data.contribs.total_stats.languages.items(),
            key=lambda x: x[1].additions + x[1].deletions,
            reverse=True,
        )[:5]
    ]

    total_out: List[CalendarDayData] = []
    for item in data.contribs.total:
        out: Dict[str, Any] = {
            "day": item.date,
            "contribs": item.stats.contribs_count,
            "commits": item.stats.commits_count,
            "issues": item.stats.issues_count,
            "prs": item.stats.prs_count,
            "reviews": item.stats.reviews_count,
            "loc_added": 0,
            "loc_changed": 0,
            "top_langs": {k: {"loc_added": 0, "loc_changed": 0} for k in top_langs},
        }

        for k, v in item.stats.languages.items():
            if k in top_langs:
                out["top_langs"][k]["loc_added"] = v.additions - v.deletions  # type: ignore
                out["top_langs"][k]["loc_changed"] = v.additions + v.deletions  # type: ignore
            out["loc_added"] += v.additions - v.deletions  # type: ignore
            out["loc_changed"] += v.additions + v.deletions  # type: ignore

        out_obj = CalendarDayData.parse_obj(out)
        total_out.append(out_obj)

    return total_out
