from typing import Any, Dict

from fastapi import APIRouter, Response, status

from src.models import WrappedPackage
from src.subscriber.processing import get_is_valid_user, query_wrapped_user
from src.utils import async_fail_gracefully

router = APIRouter()


@router.get(
    "/valid/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any]
)
@async_fail_gracefully
async def check_valid_user(response: Response, user_id: str) -> str:
    print("Checking valid user")
    out = await get_is_valid_user(user_id)
    print(out)
    return out


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
@async_fail_gracefully
async def get_wrapped_user(
    response: Response, user_id: str, year: int = 2022, no_cache: bool = False
) -> WrappedPackage:
    valid_user = await get_is_valid_user(user_id)
    if valid_user != "Valid user":
        return WrappedPackage.empty()
    return await query_wrapped_user(user_id, year, no_cache=no_cache)
