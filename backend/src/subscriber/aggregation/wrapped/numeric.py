from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

from src.models import (
    FullUserPackage,
    FullContributionDay,
    NumericData,
    ContribStats,
    MiscStats,
)


def get_contrib_stats(data: FullUserPackage) -> ContribStats:
    return ContribStats.parse_obj(
        {
            "contribs": data.contribs.total_stats.contribs_count,
            "public_contribs": data.contribs.public_stats.contribs_count
            - data.contribs.public_stats.other_count,
            "commits": data.contribs.total_stats.commits_count,
            "public_commits": data.contribs.public_stats.commits_count,
            "issues": data.contribs.total_stats.issues_count,
            "public_issues": data.contribs.public_stats.issues_count,
            "prs": data.contribs.total_stats.prs_count,
            "public_prs": data.contribs.public_stats.prs_count,
            "reviews": data.contribs.total_stats.reviews_count,
            "public_reviews": data.contribs.public_stats.reviews_count,
        }
    )


def get_misc_stats(data: FullUserPackage) -> MiscStats:
    def get_dataset_stats(
        dataset: List[FullContributionDay], subtract_other: bool
    ) -> Tuple[int, int, int]:
        """Calculates distinct days, longest streak, weekend %"""
        weekdays: Dict[int, int] = defaultdict(int)
        yeardays, distinct_days, total_contribs = {}, 0, 0
        for item in dataset:
            count = item.stats.contribs_count
            if subtract_other:
                count -= item.stats.other_count
            weekdays[item.weekday] += count
            total_contribs += item.stats.contribs_count
            if count > 0:
                date = datetime.fromisoformat(item.date)
                yeardays[date.timetuple().tm_yday - 1] = 1
                distinct_days += 1
        curr, best = 0, 0
        for i in range(366):
            best = max(best, curr)
            curr = curr + 1 if i in yeardays else 0
        longest_streak = max(best, curr)
        weekend_percent = round(100 * (weekdays[5] + weekdays[6]) / total_contribs)
        return distinct_days, longest_streak, weekend_percent

    total_days, longest_streak, weekend_percent = get_dataset_stats(
        data.contribs.total, False
    )

    (public_days, public_streak, public_weekend_percent) = get_dataset_stats(
        data.contribs.public, True
    )

    return MiscStats.parse_obj(
        {
            "total_days": str(total_days) + " Days",
            "public_total_days": str(public_days) + " Days",
            "longest_streak": str(longest_streak) + " Days",
            "public_longest_streak": str(public_streak) + " Days",
            "weekend_percent": str(weekend_percent) + "%",
            "public_weekend_percent": str(public_weekend_percent) + "%",
        }
    )


def get_numeric_data(data: FullUserPackage) -> NumericData:
    return NumericData.parse_obj(
        {"contribs": get_contrib_stats(data), "misc": get_misc_stats(data)}
    )
