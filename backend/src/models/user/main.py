from pydantic import BaseModel

from src.models.user.contribs import FullUserContributions, UserContributions
from src.models.user.follows import UserFollows

# from src.models.user.follows import UserFollows


class UserPackage(BaseModel):
    contribs: UserContributions
    # follows: UserFollows


class FullUserPackage(BaseModel):
    contribs: FullUserContributions
    follows: UserFollows
