from datetime import datetime, timedelta
from typing import Optional

from src.data.mongo.secret import get_next_key
from src.data.mongo.user import UserMetadata, get_user_metadata
from src.data.mongo.wrapped import (
    WrappedModel,
    get_wrapped_user as db_get_wrapped_user,
    lock_wrapped_user,
)
from src.models.wrapped.main import WrappedPackage
from src.publisher.processing.pubsub import publish_wrapped_user
from src.utils import alru_cache


def validate_dt(dt: Optional[datetime], td: timedelta):
    """Returns false if invalid date"""
    last_updated = dt if dt is not None else datetime(1970, 1, 1)
    time_diff = datetime.now() - last_updated
    return time_diff <= td


async def update_wrapped_user(user_id: str, year: int) -> bool:
    await lock_wrapped_user(user_id, year)
    user: Optional[UserMetadata] = await get_user_metadata(user_id)
    if user is None:
        access_token = await get_next_key("wrapped")
    else:
        access_token = user.access_token
    publish_wrapped_user(user_id, access_token, year)
    return True


@alru_cache()
async def get_wrapped_user(
    user_id: str, year: int, no_cache: bool
) -> Optional[WrappedPackage]:
    db_record: Optional[WrappedModel] = await db_get_wrapped_user(
        user_id, year, no_cache=no_cache
    )
    if db_record is None:
        await update_wrapped_user(user_id, year)
        return (False, None)  # type: ignore

    if db_record.data is None and not validate_dt(db_record.lock, timedelta(minutes=1)):
        await update_wrapped_user(user_id, year)
        return (False, None)  # type: ignore

    return (True, db_record.data)  # type: ignore
