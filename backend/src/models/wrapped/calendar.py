from typing import Dict

from pydantic import BaseModel


class CalendarLanguageDayData(BaseModel):
    loc_added: int
    loc_changed: int


class CalendarDayData(BaseModel):
    day: str
    contribs: int
    public_contribs: int
    commits: int
    public_commits: int
    issues: int
    public_issues: int
    prs: int
    public_prs: int
    reviews: int
    public_reviews: int
    loc_added: int
    public_loc_added: int
    loc_changed: int
    public_loc_changed: int
    top_langs: Dict[str, CalendarLanguageDayData]
    public_top_langs: Dict[str, CalendarLanguageDayData]
