from datetime import date, datetime, timedelta
from typing import Optional

from src.data.mongo.secret.functions import update_keys
from src.data.mongo.user import (
    FullUserModel,
    PublicUserModel,
    get_full_user as db_get_full_user,
    get_public_user as db_get_public_user,
)
from src.data.mongo.user_months import get_user_months
from src.models import UserPackage
from src.publisher.processing.pubsub import publish_user

# TODO: replace with call to subscriber so compute not on publisher
from src.subscriber.aggregation import get_user_data
from src.utils import alru_cache


def validate_dt(dt: Optional[datetime], td: timedelta):
    """Returns false if invalid date"""
    last_updated = dt if dt is not None else datetime(1970, 1, 1)
    time_diff = datetime.now() - last_updated
    return time_diff <= td


async def update_user(user_id: str, access_token: Optional[str] = None) -> bool:
    """Sends a message to pubsub to request a user update (auto cache updates)"""
    if access_token is None:
        user: Optional[PublicUserModel] = await db_get_public_user(user_id)
        if user is None:
            return False
        access_token = user.access_token
    publish_user(user_id, access_token)
    return True


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
    db_user: Optional[FullUserModel] = await db_get_full_user(
        user_id, no_cache=no_cache
    )

    if db_user is None or db_user.access_token == "":
        raise LookupError("Invalid UserId")

    need_update = not validate_dt(db_user.last_updated, timedelta(hours=6))
    recent_query = validate_dt(db_user.lock, timedelta(minutes=1))
    print("Need Update:", need_update)
    print("Recent Query:", recent_query)
    if need_update and not recent_query:
        await update_user(user_id, db_user.access_token)
        return (False, None)  # type: ignore

    user_data = await _get_user(user_id, start_date, end_date)

    if user_data is None:
        return (False, None)  # type: ignore
    return (True, user_data)  # type: ignore


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
    )
    return (True, data)  # type: ignore
