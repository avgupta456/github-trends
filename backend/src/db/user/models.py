from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator

from src.models.user.package import UserPackage

"""
Input Models
"""


class CreateUserModel(BaseModel):
    user_id: str
    access_token: str


"""
Database Models
"""


class UserModel(BaseModel):
    user_id: str
    access_token: str
    last_updated: Optional[datetime]
    raw_data: Optional[UserPackage]
    lock: Optional[datetime]

    class Config:
        validate_assignment = True

    @validator("lock", pre=True, always=True)
    def set_name(cls, lock: Union[None, bool, datetime]) -> datetime:
        if not isinstance(lock, datetime):
            return datetime(1970, 1, 1)
        return lock
