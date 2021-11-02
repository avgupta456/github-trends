from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    name: Optional[str]
    login: str
    url: str

    class Config:
        allow_none = True


class UserFollows(BaseModel):
    followers: List[User]
    following: List[User]
