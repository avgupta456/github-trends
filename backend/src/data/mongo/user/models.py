from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator

"""
Input Models
"""


class CreateUserModel(BaseModel):
    user_id: str
    access_token: str


"""
Database Models
"""


class PublicUserModel(BaseModel):
    user_id: str
    access_token: str
    private_access: Optional[bool]

    class Config:
        validate_assignment = True

    @validator("private_access", pre=True, always=True)
    def set_name(cls, private_access: bool):
        return False if private_access is None else private_access


class FullUserModel(PublicUserModel):
    user_key: Optional[str]
    last_updated: Optional[datetime]
    lock: Optional[datetime]

    @validator("lock", pre=True, always=True)
    def set_name(cls, lock: Union[None, bool, datetime]) -> datetime:
        if not isinstance(lock, datetime):
            return datetime(1970, 1, 1)
        return lock
