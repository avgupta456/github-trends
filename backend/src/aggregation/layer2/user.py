from datetime import date, timedelta
from typing import Optional, Tuple

from src.aggregation.layer0 import get_user_data
from src.data.mongo.secret.functions import update_keys
from src.data.mongo.user import PublicUserModel, get_public_user as db_get_public_user
from src.data.mongo.user_months import get_user_months
from src.models import UserPackage
from src.models.background import UpdateUserBackgroundTask
from src.utils import alru_cache

# Formerly the publisher, loads existing data here


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
) -> Tuple[bool, Tuple[Optional[UserPackage], Optional[UpdateUserBackgroundTask]]]:
    user: Optional[PublicUserModel] = await db_get_public_user(user_id)
    if user is None:
        return (False, (None, None))

    private_access = user.private_access or False
    user_data = await _get_user(user_id, private_access, start_date, end_date)
    background_task = UpdateUserBackgroundTask(
        user_id=user_id, access_token=user.access_token, private_access=private_access
    )
    return (user_data is not None, (user_data, background_task))


@alru_cache(ttl=timedelta(minutes=15))
async def get_user_demo(
    user_id: str, start_date: date, end_date: date, no_cache: bool = False
) -> Tuple[bool, UserPackage]:
    await update_keys()
    timezone_str = "US/Eastern"
    # recompute/cache but don't save to db
    data = await get_user_data(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        timezone_str=timezone_str,
        access_token=None,
        catch_errors=True,
    )
    return (True, data)
