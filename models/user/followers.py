from typing import List, Optional

from pydantic import BaseModel, Field

"""
APIResponse
"""


class APIResponse_User(BaseModel):
    """
    BaseModel which accepts:
    - name: Optional[str]
    - login: str
    - url: str
    """

    name: Optional[str]
    login: str
    url: str

    class Config:
        allow_none = True


class APIResponse_PageInfo(BaseModel):
    """
    BaseModel which accepts:
    - hasNextPage: bool
    - endCursor: str
    """

    has_next_page: bool = Field(alias="hasNextPage")
    end_cursor: Optional[str] = Field(alias="endCursor")

    class Config:
        allow_none = True


class APIResponse(BaseModel):
    """
    BaseModel which accepts:
    - totalCount: int
    - nodes: List[APIResponse_User]
    - pageInfo: APIResponse_PageInfo
    """

    nodes: List[APIResponse_User]
    page_info: APIResponse_PageInfo = Field(alias="pageInfo")


"""
EXTERNAL
"""


class User(BaseModel):
    """
    BaseModel which accepts:
    - name: Optional[str]
    - login: str
    - url: str
    """

    name: Optional[str]
    login: str
    url: str

    class Config:
        allow_none = True


class UserFollowers(BaseModel):
    """
    BaseModel which accepts:
    - followers: List[User]
    - following: List[User]
    """

    followers: List[User]
    following: List[User]
