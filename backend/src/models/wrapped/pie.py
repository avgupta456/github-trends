from typing import List, Optional

from pydantic import BaseModel


class PieDatum(BaseModel):
    id: str
    label: str
    value: int
    formatted_value: str
    color: Optional[str]


class PieData(BaseModel):
    repos_changed: List[PieDatum]
    repos_added: List[PieDatum]
    public_repos_changed: List[PieDatum]
    public_repos_added: List[PieDatum]
    langs_changed: List[PieDatum]
    langs_added: List[PieDatum]
    public_langs_changed: List[PieDatum]
    public_langs_added: List[PieDatum]
