from pydantic import BaseModel, Field


class RawCommit(BaseModel):
    additions: int
    deletions: int
    changed_files: int = Field(alias="changedFiles")
