from pydantic import BaseModel

from models.user.contribution_calendar import UserContribCalendar
from models.user.contribution_commits import UserContribCommits
from models.user.contribution_stats import UserContribStats
from models.user.follows import UserFollows


class UserPackage(BaseModel):
    """
    BaseModel which accepts:
    - contribution_calendar: UserContribCalendar
    - contribution_commits: UserContribCommits
    - contribution_stats: UserContribStats
    - follows: UserFollows
    """

    contribution_calendar: UserContribCalendar
    contribution_commits: UserContribCommits
    contribution_stats: UserContribStats
    follows: UserFollows
