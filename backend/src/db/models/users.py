from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.models.user.analytics import RawDataModel

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
    last_updated: datetime
    raw_data: Optional[RawDataModel]
    lock: bool
