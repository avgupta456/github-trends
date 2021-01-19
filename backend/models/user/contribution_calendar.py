from enum import Enum

from typing import List

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
