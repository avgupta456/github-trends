from typing import Any, Dict, List

from src.models import FullUserPackage, CalendarDayData


def get_calendar_data(data: FullUserPackage) -> List[CalendarDayData]:
    top_langs = [
        x[0]
        for x in sorted(
            data.contribs.total_stats.languages.items(),
            key=lambda x: x[1].additions + x[1].deletions,
            reverse=True,
        )[:5]
    ]

    public_top_langs = [
        x[0]
        for x in sorted(
            data.contribs.public_stats.languages.items(),
            key=lambda x: x[1].additions + x[1].deletions,
            reverse=True,
        )[:5]
    ]

    total_out: List[CalendarDayData] = []
    for all, public in zip(data.contribs.total, data.contribs.public):
        out: Dict[str, Any] = {
            "day": all.date,
            "contribs": all.stats.contribs_count,
            "public_contribs": public.stats.contribs_count - public.stats.other_count,
            "commits": all.stats.commits_count,
            "public_commits": public.stats.commits_count,
            "issues": all.stats.issues_count,
            "public_issues": public.stats.issues_count,
            "prs": all.stats.prs_count,
            "public_prs": public.stats.prs_count,
            "reviews": all.stats.reviews_count,
            "public_reviews": public.stats.reviews_count,
            "loc_added": 0,
            "public_loc_added": 0,
            "loc_changed": 0,
            "public_loc_changed": 0,
            "top_langs": {k: {"loc_added": 0, "loc_changed": 0} for k in top_langs},
            "public_top_langs": {
                k: {"loc_added": 0, "loc_changed": 0} for k in public_top_langs
            },
        }

        for k, v in all.stats.languages.items():
            if k in top_langs:
                out["top_langs"][k]["loc_added"] = v.additions - v.deletions  # type: ignore
                out["top_langs"][k]["loc_changed"] = v.additions + v.deletions  # type: ignore
            out["loc_added"] += v.additions - v.deletions  # type: ignore
            out["loc_changed"] += v.additions + v.deletions  # type: ignore

        for k, v in public.stats.languages.items():
            if k in public_top_langs:
                out["public_top_langs"][k]["loc_added"] = v.additions - v.deletions  # type: ignore
                out["public_top_langs"][k]["loc_changed"] = v.additions + v.deletions  # type: ignore
            out["public_loc_added"] += v.additions - v.deletions  # type: ignore
            out["public_loc_changed"] += v.additions + v.deletions  # type: ignore

        out_obj = CalendarDayData.parse_obj(out)
        total_out.append(out_obj)

    return total_out
