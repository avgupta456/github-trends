from datetime import date, datetime, timedelta
from typing import Tuple


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
        "all_time": (365 * 10, "All Time"),
    }

    start_str = start_date.strftime("X%m/X%d/%Y").replace("X0", "X").replace("X", "")
    end_str = end_date.strftime("X%m/X%d/%Y").replace("X0", "X").replace("X", "")
    if end_date == date.today():
        end_str = "Present"
    time_str = f"{start_str} - {end_str}"

    if time_range in duration_options:
        days, time_str = duration_options[time_range]
        end_date = date.today()
        start_date = date.today() - timedelta(days)

    return start_date, end_date, time_str


def format_number(num: int) -> str:
    if num > 10000:
        return f"~{str(num // 1000)}k lines"
    elif num > 1000:
        return f"~{str(num // 100 / 10)}k lines"
    elif num > 100:
        return f"~{str(num // 100 * 100)} lines"
    else:
        return "<100 lines"
