from collections import defaultdict
from datetime import datetime
from random import shuffle
from typing import Any, Dict, List

from src.models import FullUserPackage, SwarmData, SwarmDatum

MAX_ITEMS = 200


def date_to_seconds_since_midnight(timestamp: str) -> int:
    date = datetime.fromisoformat(timestamp)
    return (date.hour * 60 * 60) + (date.minute * 60) + date.second


def get_swarm_data(data: FullUserPackage) -> SwarmData:
    datasets = [data.contribs.total, data.contribs.public]
    full_out = {}
    for label, dataset in zip(["contribs", "public_contribs"], datasets):
        out: List[Any] = []
        counts: Dict[str, int] = defaultdict(int)
        for item in dataset:
            lists = item.lists
            lists = [lists.commits, lists.issues, lists.prs, lists.reviews]
            for type, list in zip(["commit", "issue", "pr", "review"], lists):
                shuffle(list)
                for obj in list:
                    if counts[type] > MAX_ITEMS:
                        continue

                    # timetsamp is seconds since midnight
                    timestamp = obj if isinstance(obj, str) else obj.timestamp
                    timestamp = date_to_seconds_since_midnight(timestamp)

                    _obj = {
                        "type": type,
                        "weekday": item.weekday,
                        "timestamp": timestamp,
                    }

                    out.append(SwarmDatum.parse_obj(_obj))
                    counts[type] += 1

            full_out[label] = out
    return SwarmData.parse_obj(full_out)
