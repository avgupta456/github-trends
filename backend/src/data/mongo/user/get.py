from typing import Any, Dict, Optional

from pydantic.error_wrappers import ValidationError

from src.data.mongo.main import USERS  # type: ignore
from src.data.mongo.user.models import FullUserModel, PublicUserModel
from src.utils import alru_cache


@alru_cache()
async def get_public_user(
    user_id: str, no_cache: bool = False
) -> Optional[PublicUserModel]:
    user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore

    if user is None:
        # flag is false, don't cache
        return (False, None)  # type: ignore

    try:
        return (True, PublicUserModel.parse_obj(user))  # type: ignore
    except (TypeError, KeyError, ValidationError):
        return (False, None)  # type: ignore


@alru_cache()
async def get_full_user(
    user_id: str, no_cache: bool = False
) -> Optional[FullUserModel]:
    user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore

    if user is None:
        # flag is false, don't cache
        return (False, None)  # type: ignore

    try:
        return (True, FullUserModel.parse_obj(user))  # type: ignore
    except (TypeError, KeyError, ValidationError):
        return (False, None)  # type: ignore
