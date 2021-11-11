from typing import Any, Dict, Optional

from pydantic import ValidationError

from src.utils import alru_cache
from src.data.mongo.main import WRAPPED
from src.data.mongo.wrapped.models import WrappedModel


@alru_cache()
async def get_wrapped_user(
    user_id: str, year: int, no_cache: bool = False
) -> Optional[WrappedModel]:
    user: Optional[Dict[str, Any]] = await WRAPPED.find_one({"user_id": user_id, "year": year})  # type: ignore

    if user is None:
        # flag is false, don't cache
        return (False, None)  # type: ignore

    try:
        return (True, WrappedModel.parse_obj(user))  # type: ignore
    except (TypeError, KeyError, ValidationError):
        return (False, None)  # type: ignore
