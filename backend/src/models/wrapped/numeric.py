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


class NumericData(BaseModel):
    contribs: ContribStats
