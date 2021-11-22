from pydantic import BaseModel

from src.constants import WRAPPED_VERSION
from src.models import WrappedPackage


class WrappedModel(BaseModel):
    user_id: str
    data: WrappedPackage
    private: bool = False
    version: float = WRAPPED_VERSION
