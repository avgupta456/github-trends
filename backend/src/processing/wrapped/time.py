from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Union

from src.models import DayData, MonthData, TimeDatum, UserPackage
from src.utils import format_number


def get_month_data(data: UserPackage) -> MonthData:
    months: Dict[int, Dict[str, int]] = defaultdict(
        lambda: {"contribs": 0, "loc_changed": 0}
    )

    for item in data.contribs.total:
        month = datetime.fromisoformat(item.date).month - 1
        months[month]["contribs"] += item.stats.contribs_count
        loc_changed = sum(
            x.additions + x.deletions for x in item.stats.languages.values()
        )

        months[month]["loc_changed"] += loc_changed

    out: List[TimeDatum] = []
    for k in range(12):
        v = months[k]
        _obj: Dict[str, Union[str, int]] = {
            "index": k,
            **v,
            "formatted_loc_changed": format_number(v["loc_changed"]),
        }

        out.append(TimeDatum.model_validate(_obj))

    return MonthData(months=out)


def get_day_data(data: UserPackage) -> DayData:
    days: Dict[int, Dict[str, int]] = defaultdict(
        lambda: {"contribs": 0, "loc_changed": 0}
    )

    for item in data.contribs.total:
        day = (datetime.fromisoformat(item.date).weekday() + 1) % 7
        days[day]["contribs"] += item.stats.contribs_count
        loc_changed = sum(
            x.additions + x.deletions for x in item.stats.languages.values()
        )

        days[day]["loc_changed"] += loc_changed

    out: List[TimeDatum] = []
    for k in range(7):
        v = days[k]
        _obj: Dict[str, Union[str, int]] = {
            "index": k,
            **v,
            "formatted_loc_changed": format_number(v["loc_changed"]),
        }

        out.append(TimeDatum.model_validate(_obj))

    return DayData(days=out)
