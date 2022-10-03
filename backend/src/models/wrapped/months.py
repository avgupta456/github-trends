from typing import List

from pydantic import BaseModel


class MonthDatum(BaseModel):
    month: int
    contribs: int
    loc_changed: int
    formatted_loc_changed: str


class MonthData(BaseModel):
    months: List[MonthDatum]
