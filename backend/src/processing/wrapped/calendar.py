from datetime import datetime, timedelta
from typing import Any, Dict, List

from src.models import CalendarData, CalendarDayDatum, UserPackage


def get_calendar_data(data: UserPackage, year: int) -> CalendarData:
    top_langs = [
        x[0]
        for x in sorted(
            data.contribs.total_stats.languages.items(),
            key=lambda x: x[1].additions + x[1].deletions,
            reverse=True,
        )[:5]
    ]

    total_out: List[CalendarDayDatum] = []
    items_dict = {item.date: item for item in data.contribs.total}
    for i in range(365):
        date = (datetime(year, 1, 1) + timedelta(days=i - 1)).strftime("%Y-%m-%d")
        item = items_dict.get(date)
        out: Dict[str, Any] = {
            "day": date,
            "contribs": 0,
            "commits": 0,
            "issues": 0,
            "prs": 0,
            "reviews": 0,
            "loc_added": 0,
            "loc_changed": 0,
            "top_langs": {k: {"loc_added": 0, "loc_changed": 0} for k in top_langs},
        }

        if item is not None:
            out["contribs"] = item.stats.contribs_count
            out["commits"] = item.stats.commits_count
            out["issues"] = item.stats.issues_count
            out["prs"] = item.stats.prs_count
            out["reviews"] = item.stats.reviews_count

            for k, v in item.stats.languages.items():
                if k in top_langs:
                    out["top_langs"][k]["loc_added"] = v.additions - v.deletions
                    out["top_langs"][k]["loc_changed"] = v.additions + v.deletions
                out["loc_added"] += v.additions - v.deletions
                out["loc_changed"] += v.additions + v.deletions

        out_obj = CalendarDayDatum.model_validate(out)
        total_out.append(out_obj)

    return CalendarData.model_validate({"days": total_out})
