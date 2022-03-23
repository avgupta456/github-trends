from datetime import date, timedelta
from typing import Optional

from src.data.mongo.secret.functions import update_keys
from src.data.mongo.user import PublicUserModel, get_public_user as db_get_public_user
from src.data.mongo.user_months import get_user_months
from src.models import UserPackage
from src.publisher.processing.pubsub import publish_user

# TODO: replace with call to subscriber so compute not on publisher
from src.subscriber.aggregation import get_user_data
from src.utils import alru_cache


@alru_cache()
async def update_user(user_id: str, access_token: Optional[str] = None) -> bool:
    """Sends a message to pubsub to request a user update (auto cache updates)"""
    if access_token is None:
        user: Optional[PublicUserModel] = await db_get_public_user(user_id)
        if user is None:
            return (False, False)  # type: ignore
        access_token = user.access_token
    publish_user(user_id, access_token)
    return (True, True)  # type: ignore


async def _get_user(
    user_id: str, start_date: date, end_date: date
) -> Optional[UserPackage]:
    user_months = await get_user_months(user_id, start_date, end_date)
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
) -> Optional[UserPackage]:
    await update_user(user_id)
    user_data = await _get_user(user_id, start_date, end_date)
    return (user_data is not None, user_data)  # type: ignore


@alru_cache(ttl=timedelta(minutes=15))
async def get_user_demo(
    user_id: str, start_date: date, end_date: date, no_cache: bool = False
) -> UserPackage:
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
    return (True, data)  # type: ignore
