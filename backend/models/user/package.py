from pydantic import BaseModel

from models.user.contribs import UserContributions
from models.user.follows import UserFollows


class UserPackage(BaseModel):
    contribs: UserContributions
    follows: UserFollows
