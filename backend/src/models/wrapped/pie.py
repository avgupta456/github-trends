from typing import List, Optional
from pydantic import BaseModel


class PieDatum(BaseModel):
    id: str
    label: str
    value: int
    formatted_value: str
    color: Optional[str]


class PieData(BaseModel):
    repos: List[PieDatum]
    public_repos: List[PieDatum]
    langs: List[PieDatum]
    public_langs: List[PieDatum]
