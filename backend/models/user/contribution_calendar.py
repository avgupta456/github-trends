from enum import Enum
from typing import List

from models.misc.date import Date
from pydantic import BaseModel, Field


"""
APIResponse
"""


class Quartile(str, Enum):
    """
    Emum with options: NONE, FIRST, SECOND, THIRD, FOURTH
    """

    NONE = "NONE"
    FIRST = "FIRST_QUARTILE"
    SECOND = "SECOND_QUARTILE"
    THIRD = "THIRD_QUARTILE"
    FOURTH = "FOURTH_QUARTILE"


class APIResponse_Calendar_Day(BaseModel):
    """
    BaseModel which accepts:
    - date: str
    - weekday: int
    - contributionCount: int
    - contributionLevel: Quartile
    """

    date: str
    weekday: int
    contribution_count: int = Field(alias="contributionCount")
    contribution_level: Quartile = Field(alias="contributionLevel")


class APIResponse_Calendar_Week(BaseModel):
    """
    BaseModel which accepts:
    - contribution_days: List[APIResponse_Calendar_Day]
    """

    contribution_days: List[APIResponse_Calendar_Day] = Field(alias="contributionDays")


class APIResponse_Calendar(BaseModel):
    """
    BaseModel which accepts:
    - totalContributions: int
    - weeks: List[APIResponse_Calendar_Week]
    - colors: List[str]
    """

    total_contributions: int = Field(alias="totalContributions")
    weeks: List[APIResponse_Calendar_Week]
    colors: List[str]


class APIResponse(BaseModel):
    """
    BaseModel which accepts:
    - contributionCalendar: APIResponse_Calendar
    - contributionYears: List[int]
    """

    contribution_calendar: APIResponse_Calendar = Field(alias="contributionCalendar")
    contribution_years: List[int] = Field(alias="contributionYears")


"""
EXTERNAL
"""


class ContributionDay(BaseModel):
    """
    BaseModel which accepts:
    - date: Date
    - weekday: int
    - contribution_count: int
    - contribution_level: Quartile
    """

    date: Date
    weekday: int
    contribution_count: int
    contribution_level: Quartile

    class Config:
        arbitrary_types_allowed = True


class ContributionPeriod(BaseModel):
    """
    BaseModel which accepts:
    - total_contributions: int
    - avg_contributions: float
    - days: List[ContributionDay]
    """

    total_contributions: int
    avg_contributions: float
    days: List[ContributionDay]
    num_days: int


def create_contribution_period(days: List[ContributionDay]) -> ContributionPeriod:
    num_days = len(days)
    total_contributions = sum([day.contribution_count for day in days])
    avg_contributions = total_contributions / max(num_days, 1)
    return ContributionPeriod(
        total_contributions=total_contributions,
        avg_contributions=avg_contributions,
        days=days,
        num_days=num_days,
    )


class UserContribCalendar(BaseModel):
    """
    BaseModel which accepts:
    - total_contributions: int
    - colors: List[str]
    - total: ContributionPeriod
    - months: List[ContributionPeriod]
    - weekdays: List[ContributionPeriod]
    """

    contribution_years: List[int]
    colors: List[str]
    total: ContributionPeriod
    months: List[ContributionPeriod]
    weekdays: List[ContributionPeriod]
