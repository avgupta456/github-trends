from fastapi import APIRouter, Response, status

from src.models import WrappedPackage
from src.subscriber.processing import query_wrapped_user
from src.utils import async_fail_gracefully

router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_wrapped_user(
    response: Response, user_id: str, year: int = 2022, no_cache: bool = False
) -> WrappedPackage:
    return await query_wrapped_user(user_id, year, no_cache=no_cache)
