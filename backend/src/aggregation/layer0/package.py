from datetime import date
from typing import Optional

from src.aggregation.layer0.contributions import get_contributions
from src.models import UserPackage

# from src.subscriber.aggregation.user.follows import get_user_follows


async def get_user_data(
    user_id: str,
    start_date: date,
    end_date: date,
    timezone_str: str,
    access_token: Optional[str],
    catch_errors: bool = False,
) -> UserPackage:
    """packages all processing steps for the user query"""

    contribs = await get_contributions(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        timezone_str=timezone_str,
        access_token=access_token,
        catch_errors=catch_errors,
    )
    return UserPackage(contribs=contribs)
