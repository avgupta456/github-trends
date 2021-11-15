from typing import List
from pydantic import BaseModel

from src.models.wrapped.calendar import CalendarDayData
from src.models.wrapped.pie import PieData


class WrappedPackage(BaseModel):
    calendar_data: List[CalendarDayData]
    pie_data: PieData
