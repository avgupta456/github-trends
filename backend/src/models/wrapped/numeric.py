from pydantic import BaseModel


class ContribStats(BaseModel):
    contribs: int
    public_contribs: int
    commits: int
    public_commits: int
    issues: int
    public_issues: int
    prs: int
    public_prs: int
    reviews: int
    public_reviews: int


class MiscStats(BaseModel):
    total_days: str
    public_total_days: str
    longest_streak: str
    public_longest_streak: str
    weekend_percent: str
    public_weekend_percent: str


class NumericData(BaseModel):
    contribs: ContribStats
    misc: MiscStats
