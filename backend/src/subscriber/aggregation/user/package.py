from datetime import date

from src.models import FullUserPackage, UserPackage
from src.subscriber.aggregation.user.contributions import get_contributions
from src.subscriber.aggregation.user.follows import get_user_follows

# from src.processing.user.follows import get_user_follows


async def get_user_data(
    user_id: str,
    access_token: str,
    start_date: date,
    end_date: date,
    timezone_str: str = "US/Eastern",
) -> UserPackage:
    """packages all processing steps for the user query"""

    contribs = await get_contributions(
        user_id, access_token, start_date, end_date, timezone_str
    )
    # follows = get_user_follows(user_id, access_token)
    return UserPackage(contribs=contribs)  # , follows=follows)


async def get_full_user_data(
    user_id: str,
    access_token: str,
    start_date: date,
    end_date: date,
    timezone_str: str = "US/Eastern",
) -> FullUserPackage:
    """packages all processing steps for the wrapped query"""

    contribs = await get_contributions(
        user_id, access_token, start_date, end_date, timezone_str, full=True
    )
    follows = get_user_follows(user_id, access_token)
    return FullUserPackage(contribs=contribs, follows=follows)
