from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Union

from src.models import BarData, BarDatum, FullUserPackage
from src.utils import format_number


def get_bar_data(data: FullUserPackage) -> BarData:
    full_out = {}
    datasets = [data.contribs.total, data.contribs.public]
    for label, dataset in zip(["months", "public_months"], datasets):
        months: Dict[int, Dict[str, int]] = defaultdict(
            lambda: {"contribs": 0, "loc_changed": 0}
        )
        for item in dataset:
            month = datetime.fromisoformat(item.date).month - 1
            months[month]["contribs"] += item.stats.contribs_count
            loc_changed = sum(
                [x.additions + x.deletions for x in item.stats.languages.values()]
            )
            months[month]["loc_changed"] += loc_changed

        out: List[BarDatum] = []
        for k in range(12):
            v = months[k]
            _obj: Dict[str, Union[str, int]] = {"month": k, **v}
            _obj["formatted_loc_changed"] = format_number(v["loc_changed"])
            out.append(BarDatum.parse_obj(_obj))

        full_out[label] = out
    return BarData(**full_out)
