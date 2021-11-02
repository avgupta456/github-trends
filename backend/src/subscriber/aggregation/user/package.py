from datetime import date

from src.subscriber.aggregation.user.contributions import get_contributions

# from src.processing.user.follows import get_user_follows

from src.models.user.package.main import UserPackage


async def main(
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
