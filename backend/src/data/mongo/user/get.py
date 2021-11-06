from datetime import timedelta
from typing import Any, Dict, Optional

from pydantic.error_wrappers import ValidationError

from src.data.mongo.main import USERS
from src.data.mongo.user.compression import decompress
from src.data.mongo.user.models import UserMetadata, UserModel

from src.utils import alru_cache


@alru_cache(ttl=timedelta(minutes=1))
async def get_user_metadata(
    user_id: str, no_cache: bool = False
) -> Optional[UserMetadata]:
    # excludes raw data from database query
    user: Optional[Dict[str, Any]] = await USERS.find_one(  # type: ignore
        {"user_id": user_id}, {"raw_data": 0}
    )

    if user is None:
        # flag is false, don't cache
        return (False, None)  # type: ignore

    try:
        return (True, UserMetadata.parse_obj(user))  # type: ignore
    except (TypeError, KeyError, ValidationError):
        return (False, None)  # type: ignore


@alru_cache(ttl=timedelta(minutes=1))
async def get_user_by_user_id(
    user_id: str, no_cache: bool = False
) -> Optional[UserModel]:
    user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore

    # (flag, value) output through decorator returns value

    if user is None:
        # flag is false, don't cache
        return (False, None)  # type: ignore

    if "raw_data" not in user:
        # flag is false, don't cache
        return (False, UserModel.parse_obj(user))  # type: ignore

    try:
        raw_data = decompress(user["raw_data"])
        # flag is true, do cache
        return (True, UserModel.parse_obj({**user, "raw_data": raw_data}))  # type: ignore
    except (TypeError, KeyError, ValidationError):
        return (False, UserModel.parse_obj({**user, "raw_data": None}))  # type: ignore
