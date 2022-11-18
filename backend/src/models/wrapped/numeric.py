from typing import Optional, Tuple

from pydantic import BaseModel


class ContribStats(BaseModel):
    contribs: int
    commits: int
    issues: int
    prs: int
    reviews: int
    other: int

    @classmethod
    def empty(cls) -> "ContribStats":
        return ContribStats(
            contribs=0,
            commits=0,
            issues=0,
            prs=0,
            reviews=0,
            other=0,
        )


class MiscStats(BaseModel):
    total_days: int
    longest_streak: int
    longest_streak_days: Tuple[int, int, str, str]
    longest_gap: int
    longest_gap_days: Tuple[int, int, str, str]
    weekend_percent: int
    best_day_count: int
    best_day_date: Optional[str]
    best_day_index: Optional[int]

    @classmethod
    def empty(cls) -> "MiscStats":
        return MiscStats(
            total_days=0,
            longest_streak=0,
            longest_streak_days=(0, 0, "", ""),
            longest_gap=0,
            longest_gap_days=(0, 0, "", ""),
            weekend_percent=0,
            best_day_count=0,
            best_day_date=None,
            best_day_index=None,
        )


class LOCStats(BaseModel):
    loc_additions: str
    loc_deletions: str
    loc_changed: str
    loc_added: str
    loc_additions_per_commit: int
    loc_deletions_per_commit: int
    loc_changed_per_day: int

    @classmethod
    def empty(cls) -> "LOCStats":
        return LOCStats(
            loc_additions="0",
            loc_deletions="0",
            loc_changed="0",
            loc_added="0",
            loc_additions_per_commit=0,
            loc_deletions_per_commit=0,
            loc_changed_per_day=0,
        )


class NumericData(BaseModel):
    contribs: ContribStats
    misc: MiscStats
    loc: LOCStats

    @classmethod
    def empty(cls) -> "NumericData":
        return NumericData(
            contribs=ContribStats.empty(),
            misc=MiscStats.empty(),
            loc=LOCStats.empty(),
        )
