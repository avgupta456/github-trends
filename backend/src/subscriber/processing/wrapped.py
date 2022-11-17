from datetime import date
from typing import Optional

from src.constants import OWNER, REPO
from src.data.mongo.user import PublicUserModel, get_public_user as db_get_public_user
from src.models import UserPackage, WrappedPackage
from src.subscriber.aggregation import (
    get_repo_stargazers,
    get_user_stars,
    get_valid_user,
    get_wrapped_data,
)
from src.subscriber.processing.user import query_user
from src.utils import alru_cache


async def check_user_exists(user_id: str) -> bool:
    return await get_valid_user(user_id)


async def check_user_starred_repo(
    user_id: str, owner: str = OWNER, repo: str = REPO
) -> bool:
    # Checks the repo's starred users (with cache)
    repo_stargazers = await get_repo_stargazers(owner, repo)
    if user_id in repo_stargazers:
        return True

    # Checks the user's 30 most recent starred repos (no cache)
    user_stars = await get_user_stars(user_id)
    if f"{owner}/{repo}" in user_stars:
        return True

    return False


@alru_cache()
async def query_wrapped_user(
    user_id: str, year: int, no_cache: bool = False
) -> Optional[WrappedPackage]:
    start_date, end_date = date(year, 1, 1), date(year, 12, 31)
    user: Optional[PublicUserModel] = await db_get_public_user(user_id)
    access_token = None if user is None else user.access_token
    private_access = False if user is None else user.private_access or False
    user_package: UserPackage = await query_user(
        user_id, access_token, private_access, start_date, end_date, no_cache=True
    )
    wrapped_package = get_wrapped_data(user_package, year)

    # Don't cache if incomplete
    return (not wrapped_package.incomplete, wrapped_package)  # type: ignore
