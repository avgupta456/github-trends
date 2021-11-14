from typing import List
from pydantic import BaseModel

from src.models.wrapped.calendar import CalendarDayData


class WrappedPackage(BaseModel):
    calendar_data: List[CalendarDayData]
