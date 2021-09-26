from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

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
    raw_data: Optional[Dict[str, Any]]
    lock: bool
