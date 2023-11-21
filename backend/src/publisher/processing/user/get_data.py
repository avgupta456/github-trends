from datetime import date, timedelta
from typing import Optional, Tuple

from src.data.mongo.secret.functions import update_keys
from src.data.mongo.user import PublicUserModel, get_public_user as db_get_public_user
from src.data.mongo.user_months import get_user_months
from src.models import UserPackage

# TODO: replace with call to subscriber so compute not on publisher
from src.subscriber.aggregation import get_user_data
from src.utils import alru_cache


@alru_cache()
async def update_user(
    user_id: str, access_token: Optional[str], private_access: bool
) -> Tuple[bool, bool]:
    """Sends a message to pubsub to request a user update (auto cache updates)"""
    # await publish_user(user_id, access_token, private_access)
    return (True, True)


async def _get_user(
    user_id: str, private_access: bool, start_date: date, end_date: date
) -> Optional[UserPackage]:
    user_months = await get_user_months(user_id, private_access, start_date, end_date)
    if len(user_months) == 0:
        return None

    user_data = user_months[0].data
    for user_month in user_months[1:]:
        user_data += user_month.data

    # TODO: handle timezone_str here
    return user_data.trim(start_date, end_date)


@alru_cache()
async def get_user(
    user_id: str,
    start_date: date,
    end_date: date,
    no_cache: bool = False,
) -> Tuple[bool, Optional[UserPackage]]:
    user: Optional[PublicUserModel] = await db_get_public_user(user_id)
    if user is None:
        return (False, None)

    private_access = user.private_access or False
    await update_user(user_id, user.access_token, private_access)
    user_data = await _get_user(user_id, private_access, start_date, end_date)
    return (user_data is not None, user_data)


@alru_cache(ttl=timedelta(minutes=15))
async def get_user_demo(
    user_id: str, start_date: date, end_date: date, no_cache: bool = False
) -> Tuple[bool, UserPackage]:
    await update_keys()
    timezone_str = "US/Eastern"
    data = await get_user_data(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        timezone_str=timezone_str,
        access_token=None,
        catch_errors=True,
    )
    return (True, data)
