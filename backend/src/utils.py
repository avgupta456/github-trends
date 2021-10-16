from datetime import datetime, date, timedelta
from typing import Tuple, Optional

from src.constants import OAUTH_CLIENT_ID, OAUTH_REDIRECT_URI


def get_redirect_url(private: bool = False, user_id: Optional[str] = None) -> str:
    url = (
        "https://github.com/login/oauth/authorize?client_id="
        + OAUTH_CLIENT_ID
        + "&redirect_uri="
        + OAUTH_REDIRECT_URI
        + "/redirect"
    )
    if private:
        url += "&scope=user,repo"
    if user_id is not None:
        url += "&login=" + user_id
    return url


def date_to_datetime(
    dt: date, hour: int = 0, minute: int = 0, second: int = 0
) -> datetime:

    return datetime(dt.year, dt.month, dt.day, hour, minute, second)


# returns start date, end date, string representing time range
def use_time_range(
    time_range: str, start_date: date, end_date: date
) -> Tuple[date, date, str]:
    duration_options = {
        "one_month": (30, "Past 1 Month"),
        "three_months": (90, "Past 3 Months"),
        "six_months": (180, "Past 6 Months"),
        "one_year": (365, "Past 1 Year"),
    }

    start_str = start_date.strftime("X%m/X%d/%Y").replace("X0", "X").replace("X", "")
    end_str = end_date.strftime("X%m/X%d/%Y").replace("X0", "X").replace("X", "")
    if end_date == date.today():
        end_str = "Present"
    time_str = start_str + " - " + end_str

    if time_range in duration_options:
        days, time_str = duration_options[time_range]
        end_date = date.today()
        start_date = date.today() - timedelta(days)

    return start_date, end_date, time_str
