from typing import List

from pydantic import BaseModel


class BarDatum(BaseModel):
    month: int
    contribs: int
    loc_changed: int
    formatted_loc_changed: str


class BarData(BaseModel):
    months: List[BarDatum]
    public_months: List[BarDatum]
