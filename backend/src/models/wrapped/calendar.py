from typing import Dict, List

from pydantic import BaseModel


class CalendarLanguageDayDatum(BaseModel):
    loc_added: int
    loc_changed: int


class CalendarDayDatum(BaseModel):
    day: str
    contribs: int
    commits: int
    issues: int
    prs: int
    reviews: int
    loc_added: int
    loc_changed: int
    top_langs: Dict[str, CalendarLanguageDayDatum]


class CalendarData(BaseModel):
    days: List[CalendarDayDatum]

    @classmethod
    def empty(cls) -> "CalendarData":
        return CalendarData(days=[])
