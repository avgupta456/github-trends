from typing import List

from pydantic import BaseModel


class SwarmDatum(BaseModel):
    type: str
    weekday: int
    timestamp: int


class SwarmData(BaseModel):
    contribs: List[SwarmDatum]
    public_contribs: List[SwarmDatum]
