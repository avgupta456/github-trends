from typing import Any, Dict, Optional

from fastapi import APIRouter, Response, status

from src.aggregation.layer2 import get_is_valid_user
from src.models import WrappedPackage
from src.processing.wrapped import query_wrapped_user
from src.utils import async_fail_gracefully

router = APIRouter()


@router.get(
    "/valid/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any]
)
@async_fail_gracefully
async def check_valid_user(response: Response, user_id: str) -> str:
    return await get_is_valid_user(user_id)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
@async_fail_gracefully
async def get_wrapped_user(
    response: Response, user_id: str, year: int = 2024, no_cache: bool = False
) -> Optional[WrappedPackage]:
    valid_user = await get_is_valid_user(user_id)
    if "Valid user" not in valid_user:
        return WrappedPackage.empty()

    return await query_wrapped_user(user_id, year, no_cache=no_cache)
