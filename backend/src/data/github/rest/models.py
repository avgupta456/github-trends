from datetime import datetime
from pydantic import BaseModel


class RawCommit(BaseModel):
    timestamp: datetime
    node_id: str
