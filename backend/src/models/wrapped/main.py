from pydantic import BaseModel

from src.models.user.contribs import UserContributions


class WrappedPackage(BaseModel):
    user_data: UserContributions
