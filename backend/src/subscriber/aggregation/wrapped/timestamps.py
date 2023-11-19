from datetime import datetime
from random import shuffle
from typing import Any, List

from src.models import TimestampData, TimestampDatum, UserPackage

MAX_ITEMS = 200


def date_to_seconds_since_midnight(date: datetime) -> int:
    return (date.hour * 60 * 60) + (date.minute * 60) + date.second


def get_timestamp_data(data: UserPackage) -> TimestampData:
    out: List[Any] = []
    for item in data.contribs.total:
        lists = item.lists
        lists = [lists.commits, lists.issues, lists.prs, lists.reviews]
        for type, list in zip(["commit", "issue", "pr", "review"], lists):
            out.extend(
                {
                    "type": type,
                    "weekday": item.weekday,
                    "timestamp": date_to_seconds_since_midnight(obj),
                }
                for obj in list
            )

    shuffle(out)
    out = out[:MAX_ITEMS]
    out = [TimestampDatum.model_validate(x) for x in out]

    return TimestampData(contribs=out)
