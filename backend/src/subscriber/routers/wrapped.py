from fastapi import APIRouter, Response, status

from src.models import WrappedPackage
from src.subscriber.processing import (
    check_github_user_exists,
    check_db_user_exists,
    check_user_starred_repo,
    query_wrapped_user,
)
from src.utils import async_fail_gracefully

router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_wrapped_user(
    response: Response, user_id: str, year: int = 2022, no_cache: bool = False
) -> WrappedPackage:
    valid_github_user = await check_github_user_exists(user_id)
    if not valid_github_user:
        data = WrappedPackage.empty()
        data.message = "User not found"
        return data

    valid_db_user = await check_db_user_exists(user_id)
    user_starred = await check_user_starred_repo(user_id)
    if not user_starred and not valid_db_user:
        data = WrappedPackage.empty()
        data.message = "User has not starred GitHub Trends"
        return data

    data = await query_wrapped_user(user_id, year, no_cache=no_cache)
    return data
