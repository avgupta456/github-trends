from datetime import datetime

from pydantic import BaseModel

from src.models import UserPackage


class UserMonth(BaseModel):
    user_id: str
    month: datetime
    version: float
    complete: bool
    data: UserPackage
