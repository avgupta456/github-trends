from typing import Any, Dict, Optional, Tuple

from pydantic import ValidationError

from src.data.mongo.main import USERS
from src.data.mongo.user.models import FullUserModel, PublicUserModel
from src.utils import alru_cache


@alru_cache()
async def get_public_user(
    user_id: str, no_cache: bool = False
) -> Tuple[bool, Optional[PublicUserModel]]:
    user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})
    if user is None:
        # flag is false, don't cache
        return (False, None)
    try:
        return (True, PublicUserModel.model_validate(user))
    except (TypeError, KeyError, ValidationError):
        return (False, None)


@alru_cache()
async def get_full_user(
    user_id: str, no_cache: bool = False
) -> Tuple[bool, Optional[FullUserModel]]:
    user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})

    if user is None:
        # flag is false, don't cache
        return (False, None)

    try:
        return (True, FullUserModel.model_validate(user))
    except (TypeError, KeyError, ValidationError):
        return (False, None)
