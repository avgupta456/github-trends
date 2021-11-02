from pydantic import BaseModel

from src.models.user.package.contribs import UserContributions

# from src.models.user.follows import UserFollows


class UserPackage(BaseModel):
    contribs: UserContributions
    # follows: UserFollows
