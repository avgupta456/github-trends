from datetime import datetime
from typing import Any, List

from src.models import FullUserPackage, SwarmData, SwarmDatum


def date_to_seconds_since_midnight(date: datetime) -> int:
    return (date.hour * 60 * 60) + (date.minute * 60) + date.second


def get_swarm_data(data: FullUserPackage) -> SwarmData:
    datasets = [data.contribs.total, data.contribs.public]
    full_out = {}
    for label, dataset in zip(["contribs", "public_contribs"], datasets):
        out: List[Any] = []
        for item in dataset:
            lists = item.lists
            lists = [lists.commits, lists.issues, lists.prs, lists.reviews]
            for type, list in zip(["commit", "issue", "pr", "review"], lists):
                for obj in list:
                    weekday = item.weekday
                    timestamp = obj if isinstance(obj, str) else obj.timestamp
                    timestamp = datetime.fromisoformat(timestamp)
                    timestamp = date_to_seconds_since_midnight(timestamp)
                    _obj = {"type": type, "weekday": weekday, "timestamp": timestamp}
                    out.append(SwarmDatum.parse_obj(_obj))
            full_out[label] = out
    return SwarmData.parse_obj(full_out)
