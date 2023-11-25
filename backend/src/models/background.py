from datetime import date
from typing import Optional

from pydantic import BaseModel


class UpdateUserBackgroundTask(BaseModel):
    user_id: str
    access_token: Optional[str]
    private_access: bool
    start_date: Optional[date]
    end_date: Optional[date]
