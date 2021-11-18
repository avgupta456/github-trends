from datetime import date
from typing import Optional

from src.models import FullUserPackage, UserPackage
from src.subscriber.aggregation.user.contributions import get_contributions
from src.subscriber.aggregation.user.follows import get_user_follows

# from src.processing.user.follows import get_user_follows


async def get_user_data(
    user_id: str,
    start_date: date,
    end_date: date,
    timezone_str: str,
    access_token: Optional[str],
) -> UserPackage:
    """packages all processing steps for the user query"""

    contribs = await get_contributions(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        timezone_str=timezone_str,
        access_token=access_token,
    )
    return UserPackage(contribs=contribs)


async def get_full_user_data(
    user_id: str,
    start_date: date,
    end_date: date,
    timezone_str: str,
    access_token: Optional[str],
) -> FullUserPackage:
    """packages all processing steps for the wrapped query"""

    contribs = await get_contributions(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        timezone_str=timezone_str,
        full=True,
        access_token=access_token,
    )
    follows = get_user_follows(user_id=user_id, access_token=access_token)
    return FullUserPackage(contribs=contribs, follows=follows)
