from datetime import date

from src.models import WrappedPackage
from src.subscriber.aggregation.user.package import main as get_data
from src.subscriber.aggregation.wrapped.calendar import get_calendar_data

# from src.processing.user.follows import get_user_follows


async def main(
    user_id: str,
    access_token: str,
    year: int,
) -> WrappedPackage:
    """packages all processing steps for the user query"""
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    timezone_str = "US/Eastern"

    user_package = await get_data(
        user_id, access_token, start_date, end_date, timezone_str
    )

    calendar_data = get_calendar_data(user_package)

    return WrappedPackage(calendar_data=calendar_data)
