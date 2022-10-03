from collections import defaultdict
from datetime import datetime
from random import shuffle
from typing import Any, Dict, List

from src.models import SwarmData, SwarmDatum, UserPackage

MAX_ITEMS = 200


def date_to_seconds_since_midnight(date: datetime) -> int:
    return (date.hour * 60 * 60) + (date.minute * 60) + date.second


def get_swarm_data(data: UserPackage) -> SwarmData:
    out: List[Any] = []
    counts: Dict[str, int] = defaultdict(int)
    for item in data.contribs.total:
        lists = item.lists
        lists = [lists.commits, lists.issues, lists.prs, lists.reviews]
        for type, list in zip(["commit", "issue", "pr", "review"], lists):
            shuffle(list)
            for obj in list:
                if counts[type] > MAX_ITEMS:
                    continue

                _obj = {
                    "type": type,
                    "weekday": item.weekday,
                    "timestamp": date_to_seconds_since_midnight(obj),
                }

                out.append(SwarmDatum.parse_obj(_obj))
                counts[type] += 1

    return SwarmData(contribs=out)
