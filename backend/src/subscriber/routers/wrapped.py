from fastapi import APIRouter, Response, status

from src.models import WrappedPackage
from src.subscriber.processing import (
    check_db_user_exists,
    check_github_user_exists,
    check_user_starred_repo,
    query_wrapped_user,
)
from src.utils import async_fail_gracefully

router = APIRouter()


@router.get("/valid/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def check_valid_user(response: Response, user_id: str) -> str:
    valid_github_user = await check_github_user_exists(user_id)
    if not valid_github_user:
        return "GitHub user not found"

    valid_db_user = await check_db_user_exists(user_id)
    user_starred = await check_user_starred_repo(user_id)
    if not (user_starred or valid_db_user):
        return "Repo not starred"

    return "Valid user"


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_wrapped_user(
    response: Response, user_id: str, year: int = 2022, no_cache: bool = False
) -> WrappedPackage:
    # Must be a valid user
    if not await check_github_user_exists(user_id):
        return WrappedPackage.empty()

    # If starred GitHub repo, return wrapped data
    if await check_user_starred_repo(user_id):
        return await query_wrapped_user(user_id, year, no_cache=no_cache)

    # If GitHub Trends user, return wrapped data
    if await check_db_user_exists(user_id):
        return await query_wrapped_user(user_id, year, no_cache=no_cache)

    # If both fail, return empty wrapped data
    return WrappedPackage.empty()
