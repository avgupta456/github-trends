from typing import List, Optional

from pydantic import BaseModel, Field

from src.models import User


class PageInfo(BaseModel):
    has_next_page: bool = Field(alias="hasNextPage")
    end_cursor: Optional[str] = Field(alias="endCursor")

    class Config:
        allow_none = True


class RawFollows(BaseModel):
    nodes: List[User]
    page_info: PageInfo = Field(alias="pageInfo")
