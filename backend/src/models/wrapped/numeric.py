from typing import Tuple

from pydantic import BaseModel


class ContribStats(BaseModel):
    contribs: int
    commits: int
    issues: int
    prs: int
    reviews: int
    other: int


class MiscStats(BaseModel):
    total_days: int
    longest_streak: int
    longest_streak_days: Tuple[int, int, str, str]
    longest_gap: int
    longest_gap_days: Tuple[int, int, str, str]
    weekend_percent: int


class LOCStats(BaseModel):
    loc_additions: str
    loc_deletions: str
    loc_changed: str
    loc_added: str
    loc_additions_per_commit: int
    loc_deletions_per_commit: int
    loc_changed_per_day: int


class NumericData(BaseModel):
    contribs: ContribStats
    misc: MiscStats
    loc: LOCStats
