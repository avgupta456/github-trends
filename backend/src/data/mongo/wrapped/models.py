from datetime import datetime

from pydantic import BaseModel

from src.constants import WRAPPED_VERSION
from src.models import WrappedPackage


class WrappedModel(BaseModel):
    user_id: str
    data: WrappedPackage
    lock: datetime
    version: float = WRAPPED_VERSION
