from typing import Optional

from pydantic import BaseModel, validator


class PublicUserModel(BaseModel):
    user_id: str
    access_token: str
    private_access: Optional[bool]

    class Config:
        from_attributes = True
        validate_assignment = True

    @validator("private_access", pre=True, always=True)
    def set_name(cls, private_access: Optional[bool]):
        return False if private_access is None else private_access


class FullUserModel(PublicUserModel):
    user_key: Optional[str]
