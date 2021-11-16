from typing import List

from pydantic import BaseModel

from src.models.wrapped.bar import BarData
from src.models.wrapped.calendar import CalendarDayData
from src.models.wrapped.pie import PieData
from src.models.wrapped.swarm import SwarmData


class WrappedPackage(BaseModel):
    bar_data: BarData
    calendar_data: List[CalendarDayData]
    pie_data: PieData
    swarm_data: SwarmData
