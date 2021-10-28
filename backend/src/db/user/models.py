from datetime import datetime
from typing import Optional

from pydantic import BaseModel

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
    lock: Optional[bool]
