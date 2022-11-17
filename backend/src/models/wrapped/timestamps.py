from typing import List

from pydantic import BaseModel


class TimestampDatum(BaseModel):
    type: str
    weekday: int
    timestamp: int


class TimestampData(BaseModel):
    contribs: List[TimestampDatum]

    @classmethod
    def empty(cls) -> "TimestampData":
        return TimestampData(contribs=[])
