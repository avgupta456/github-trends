from typing import Dict

from pydantic import BaseModel


class CalendarLanguageDayData(BaseModel):
    loc_added: int
    loc_changed: int


class CalendarDayData(BaseModel):
    day: str
    contribs: int
    commits: int
    issues: int
    prs: int
    reviews: int
    loc_added: int
    loc_changed: int
    top_langs: Dict[str, CalendarLanguageDayData]
