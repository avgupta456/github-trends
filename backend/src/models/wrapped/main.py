from pydantic import BaseModel

from src.models.wrapped.calendar import CalendarData
from src.models.wrapped.langs import LangData
from src.models.wrapped.numeric import NumericData
from src.models.wrapped.repos import RepoData
from src.models.wrapped.time import DayData, MonthData
from src.models.wrapped.timestamps import TimestampData


class WrappedPackage(BaseModel):
    month_data: MonthData
    day_data: DayData
    calendar_data: CalendarData
    numeric_data: NumericData
    repo_data: RepoData
    lang_data: LangData
    timestamp_data: TimestampData
