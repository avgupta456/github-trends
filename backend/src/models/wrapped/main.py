from typing import Any, Dict

from pydantic import BaseModel


class WrappedPackage(BaseModel):
    data: Dict[str, Any]
