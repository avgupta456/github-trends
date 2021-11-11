from datetime import datetime

from pydantic import BaseModel

from src.models import WrappedPackage


class WrappedModel(BaseModel):
    user_id: str
    data: WrappedPackage
    lock: datetime
    version: int = 1
