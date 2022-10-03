from typing import List

from pydantic import BaseModel

from src.models.wrapped.month import MonthData
from src.models.wrapped.calendar import CalendarDayData
from src.models.wrapped.numeric import NumericData
from src.models.wrapped.pie import PieData
from src.models.wrapped.timestamp import TimestampData


class WrappedPackage(BaseModel):
    month_data: MonthData
    calendar_data: List[CalendarDayData]
    numeric_data: NumericData
    pie_data: PieData
    timestamp_data: TimestampData
