from typing import List

from pydantic import BaseModel


class SecretModel(BaseModel):
    project: str
    access_tokens: List[str]
