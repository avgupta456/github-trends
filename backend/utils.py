from datetime import datetime, date


def date_to_datetime(
    dt: date, hour: int = 0, minute: int = 0, second: int = 0
) -> datetime:

    return datetime(dt.year, dt.month, dt.day, hour, minute, second)
