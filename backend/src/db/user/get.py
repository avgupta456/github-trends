from typing import Any, Dict, Optional

from pydantic.error_wrappers import ValidationError

from src.db.mongodb import USERS
from src.db.user.compression import decompress
from src.db.user.models import UserMetadata, UserModel

from src.helper.alru_cache import alru_cache


"""
Raw Get Methods
"""


@alru_cache(max_size=128)
async def _get_user_by_id(
    user_id: str, no_cache: bool = False
) -> Optional[Dict[str, Any]]:
    return (True, await USERS.find_one({"user_id": user_id}))  # type: ignore


@alru_cache(max_size=128)
async def _get_user_by_access_token(
    access_token: str, no_cache: bool = False
) -> Optional[Dict[str, Any]]:
    return (True, await USERS.find_one({"access_token": access_token}))  # type: ignore


"""
External Get Methods
"""


@alru_cache(max_size=128)
async def get_user_metadata(
    user_id: str, no_cache: bool = False
) -> Optional[UserMetadata]:
    user = await _get_user_by_id(user_id, no_cache)

    if user is None:
        # flag is false, don't cache
        return (False, None)  # type: ignore

    try:
        return (True, UserMetadata.parse_obj(user))  # type: ignore
    except (TypeError, KeyError, ValidationError):
        return (False, None)  # type: ignore


@alru_cache(max_size=128)
async def get_user_by_user_id(
    user_id: str, no_cache: bool = False
) -> Optional[UserModel]:
    user = await _get_user_by_id(user_id, no_cache)

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


@alru_cache(max_size=128)
async def get_user_by_access_token(
    access_token: str, no_cache: bool = False
) -> Optional[UserModel]:
    user = await _get_user_by_access_token(access_token, no_cache)

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
