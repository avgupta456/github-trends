from __future__ import annotations

from datetime import datetime, timedelta

from typing import Union


class Date:
    """Date object using datetime"""

    def __init__(self, date: Union[str, datetime]) -> None:
        self.date_obj: datetime
        if isinstance(date, datetime):
            date = "-".join([str(date.year), str(date.month), str(date.day)])
        date_str: str = date.split("T")[0] if "T" in date else date
        self.date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    def __str__(self) -> str:
        return str(self.date_obj.date())

    def __add__(self, other: int) -> Date:
        new_date: Date = Date(self.date_obj + timedelta(days=other))
        return new_date

    def __sub__(self, other: int) -> Date:
        new_date: Date = Date(self.date_obj - timedelta(days=other))
        return new_date

    def __lt__(self, other: Date) -> bool:
        return self.date_obj < other.date_obj


today = Date(datetime.now())