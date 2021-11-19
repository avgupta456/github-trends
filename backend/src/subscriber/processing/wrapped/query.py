from typing import Optional

from src.data.mongo.secret import update_keys
from src.data.mongo.user import get_user_metadata, UserMetadata
from src.data.mongo.wrapped import (
    get_wrapped_user as db_get_wrapped_user,
    set_wrapped_user,
    WrappedModel,
)
from src.models import WrappedPackage
from src.subscriber.aggregation import get_wrapped_data
from src.utils import alru_cache


@alru_cache()
async def update_wrapped_user(user_id: str, year: int) -> WrappedPackage:
    await update_keys()
    user: Optional[UserMetadata] = await get_user_metadata(user_id)
    access_token = None if user is None else user.access_token
    wrapped_package: WrappedPackage = await get_wrapped_data(
        user_id=user_id, year=year, access_token=access_token
    )
    await set_wrapped_user(user_id, year, wrapped_package)
    return (True, wrapped_package)  # type: ignore


# NOTE: query user from wrapped subscriber router, not PubSub


@alru_cache()
async def query_wrapped_user(
    user_id: str, year: int, no_cache: bool = False
) -> WrappedPackage:
    db_record: Optional[WrappedModel] = await db_get_wrapped_user(
        user_id, year, no_cache=True
    )

    if db_record is None or db_record.data is None:
        wrapped_data = await update_wrapped_user(user_id, year)
    else:
        wrapped_data = db_record.data

    return (True, wrapped_data)  # type: ignore
