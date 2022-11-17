from typing import List

from pydantic import BaseModel


class LangDatum(BaseModel):
    id: str
    label: str
    value: int
    formatted_value: str
    color: str


class LangData(BaseModel):
    langs_changed: List[LangDatum]
    langs_added: List[LangDatum]

    @classmethod
    def empty(cls) -> "LangData":
        return LangData(langs_changed=[], langs_added=[])
