from datetime import date, timedelta
from typing import Any, Dict

from packaging.user import main as get_data

from analytics.user.contribs_per_day import (
    get_contribs_per_day,
    get_contribs_per_repo_per_day,
)


from helper.gather import gather


def main(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Dict[str, Any]:
    data = get_data(user_id, start_date, end_date, timezone_str)

    [contribs_per_day, contribs_per_repo_per_day] = gather(
        funcs=[get_contribs_per_day, get_contribs_per_repo_per_day],
        args_dicts=[{"data": data} for _ in range(2)],
    )

    return {
        "raw": data,
        "contribs_per_day": contribs_per_day,
        "contribs_per_repo_per_day": contribs_per_repo_per_day,
    }
