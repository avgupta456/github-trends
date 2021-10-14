from typing import Any, Dict, Optional

from pydantic.error_wrappers import ValidationError

from src.db.mongodb import USERS
from src.db.functions.compression import decompress
from src.db.models.users import UserModel

from src.helper.alru_cache import alru_cache


"""
Raw Get Methods
"""


@alru_cache(max_size=128)
async def get_user_by_user_id(
    user_id: str, use_cache: bool = True
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


@alru_cache(max_size=128)
async def get_user_by_access_token(
    access_token: str, use_cache: bool = True
) -> Optional[UserModel]:
    user: Optional[Dict[str, Any]] = await USERS.find_one(  # type: ignore
        {"access_token": access_token}
    )

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
