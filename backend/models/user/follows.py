from typing import List, Optional

from pydantic import BaseModel, Field

"""
APIResponse
"""


class User(BaseModel):
    name: Optional[str]
    login: str
    url: str

    class Config:
        allow_none = True


class PageInfo(BaseModel):
    has_next_page: bool = Field(alias="hasNextPage")
    end_cursor: Optional[str] = Field(alias="endCursor")

    class Config:
        allow_none = True


class RawFollows(BaseModel):
    nodes: List[User]
    page_info: PageInfo = Field(alias="pageInfo")


class UserFollows(BaseModel):
    followers: List[User]
    following: List[User]
