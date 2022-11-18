from typing import List

from pydantic import BaseModel


class TimeDatum(BaseModel):
    index: int
    contribs: int
    loc_changed: int
    formatted_loc_changed: str


class MonthData(BaseModel):
    months: List[TimeDatum]

    @classmethod
    def empty(cls) -> "MonthData":
        return MonthData(months=[])


class DayData(BaseModel):
    days: List[TimeDatum]

    @classmethod
    def empty(cls) -> "DayData":
        return DayData(days=[])
