from datetime import date, timedelta
from typing import Any

from packaging.user import main as get_data

from analytics.user.contribs_per_day import get_contribs_per_day


def main(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Any:
    data = get_data(user_id, start_date, end_date, timezone_str)

    contribs_per_day = get_contribs_per_day(data)

    return {"contribs_per_day": contribs_per_day}
