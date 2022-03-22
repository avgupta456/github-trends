from datetime import date
from typing import Optional

from src.models import WrappedPackage
from src.subscriber.aggregation.user.package import get_user_data
from src.subscriber.aggregation.wrapped.bar import get_bar_data
from src.subscriber.aggregation.wrapped.calendar import get_calendar_data
from src.subscriber.aggregation.wrapped.numeric import get_numeric_data
from src.subscriber.aggregation.wrapped.pie import get_pie_data

# from src.processing.user.follows import get_user_follows


async def main(
    user_id: str,
    year: int,
    access_token: Optional[str],
) -> WrappedPackage:
    """packages all processing steps for the user query"""
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    timezone_str = "US/Eastern"

    user_package = await get_user_data(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        timezone_str=timezone_str,
        access_token=access_token,
    )

    bar_data = get_bar_data(user_package)
    calendar_data = get_calendar_data(user_package)
    numeric_data = get_numeric_data(user_package)
    pie_data = get_pie_data(user_package)

    return WrappedPackage(
        bar_data=bar_data,
        calendar_data=calendar_data,
        numeric_data=numeric_data,
        pie_data=pie_data,
    )
