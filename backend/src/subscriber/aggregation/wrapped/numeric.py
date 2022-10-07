from collections import defaultdict
from datetime import datetime
from typing import Dict

from src.models import ContribStats, LOCStats, MiscStats, NumericData, UserPackage


def get_contrib_stats(data: UserPackage) -> ContribStats:
    return ContribStats.parse_obj(
        {
            "contribs": data.contribs.total_stats.contribs_count,
            "commits": data.contribs.total_stats.commits_count,
            "issues": data.contribs.total_stats.issues_count,
            "prs": data.contribs.total_stats.prs_count,
            "reviews": data.contribs.total_stats.reviews_count,
            "other": data.contribs.total_stats.other_count,
        }
    )


def get_misc_stats(data: UserPackage, year: int) -> MiscStats:
    weekdays: Dict[int, int] = defaultdict(int)
    yeardays, distinct_days, total_contribs = {}, 0, 0
    for item in data.contribs.total:
        count = item.stats.contribs_count
        weekdays[item.weekday] += count
        total_contribs += item.stats.contribs_count
        if count > 0:
            date = datetime.fromisoformat(item.date)
            yeardays[date.timetuple().tm_yday - 1] = 1
            distinct_days += 1
    curr, best, best_dates = 0, 0, (1, 1)
    for i in range(366):
        curr = curr + 1 if i in yeardays else 0
        if curr > best:
            best = curr
            best_dates = (i - curr + 2, i + 1)
    longest_streak = max(best, curr)
    longest_streak_days = (
        best_dates[0],
        best_dates[1],
        datetime.fromordinal(max(1, best_dates[0])).strftime("%b %d"),
        datetime.fromordinal(max(1, best_dates[1])).strftime("%b %d"),
    )
    curr, best, best_dates = 0, 0, (1, 1)
    days = (datetime.now() - datetime(year, 1, 1)).days
    for i in range(min(days, 365)):
        curr = 0 if i in yeardays else curr + 1
        if curr > best:
            best = curr
            best_dates = (i - curr + 2, i + 1)
    longest_gap = max(best, curr)
    longest_gap_days = (
        best_dates[0],
        best_dates[1],
        datetime.fromordinal(max(1, best_dates[0])).strftime("%b %d"),
        datetime.fromordinal(max(1, best_dates[1])).strftime("%b %d"),
    )
    weekend_percent = (weekdays[0] + weekdays[6]) / max(1, total_contribs)

    return MiscStats.parse_obj(
        {
            "total_days": distinct_days,
            "longest_streak": longest_streak,
            "longest_streak_days": longest_streak_days,
            "longest_gap": longest_gap,
            "longest_gap_days": longest_gap_days,
            "weekend_percent": round(100 * weekend_percent),
        }
    )


def format_loc_number(number: int) -> str:
    if number < 1e3:
        return str(100 * round(number / 100))
    if number < 1e6:
        return str(round(number / 1e3)) + ",000"
    return str(round(number / 1e6)) + ",000,000"


def get_loc_stats(data: UserPackage) -> LOCStats:
    dataset = data.contribs.total_stats.languages.values()
    return LOCStats.parse_obj(
        {
            "loc_additions": format_loc_number(sum([x.additions for x in dataset])),
            "loc_deletions": format_loc_number(sum([x.deletions for x in dataset])),
            "loc_changed": format_loc_number(
                sum([x.additions + x.deletions for x in dataset])
            ),
            "loc_added": format_loc_number(
                sum([x.additions - x.deletions for x in dataset])
            ),
            "loc_additions_per_commit": round(
                sum([x.additions for x in dataset])
                / max(1, data.contribs.total_stats.commits_count)
            ),
            "loc_deletions_per_commit": round(
                sum([x.deletions for x in dataset])
                / max(1, data.contribs.total_stats.commits_count)
            ),
            "loc_changed_per_day": round(
                sum([x.additions + x.deletions for x in dataset]) / 365
            ),
        }
    )


def get_numeric_data(data: UserPackage, year: int) -> NumericData:
    return NumericData.parse_obj(
        {
            "contribs": get_contrib_stats(data),
            "misc": get_misc_stats(data, year),
            "loc": get_loc_stats(data),
        }
    )
