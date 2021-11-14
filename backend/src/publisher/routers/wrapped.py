from typing import Optional

from fastapi import APIRouter, Response, status

from src.models import WrappedPackage
from src.publisher.processing import get_wrapped_user
from src.utils import async_fail_gracefully

router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_wrapped_user_endpoint(
    response: Response,
    user_id: str,
    year: int = 2021,
    no_cache: bool = False,
) -> Optional[WrappedPackage]:
    return await get_wrapped_user(user_id, year, no_cache)
