from datetime import datetime
from typing import Optional

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
    private_access: Optional[bool]
    last_updated: Optional[datetime]
    raw_data: Optional[UserPackage]
    lock: Optional[bool]

    class Config:
        validate_assignment = True

    @validator("private_access", pre=True, always=True)
    def set_name(cls, private_access: bool):
        return False if private_access is None else private_access
