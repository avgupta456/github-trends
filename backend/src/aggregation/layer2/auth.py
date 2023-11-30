from datetime import timedelta
from typing import Optional, Tuple

from src.aggregation.layer1.auth import (
    get_repo_stargazers,
    get_user_stars,
    get_valid_db_user,
    get_valid_github_user,
)
from src.constants import OWNER, REPO, USER_BLACKLIST, USER_WHITELIST
from src.data.github.rest import RESTError
from src.utils import alru_cache


async def check_github_user_exists(user_id: str) -> Optional[str]:
    return await get_valid_github_user(user_id)


async def check_db_user_exists(user_id: str) -> bool:
    return await get_valid_db_user(user_id)


async def check_user_starred_repo(
    user_id: str, owner: str = OWNER, repo: str = REPO
) -> bool:
    # Checks the repo's starred users (with cache)
    try:
        repo_stargazers = await get_repo_stargazers(owner, repo)
        if user_id in repo_stargazers:
            return True
    except RESTError:
        return True  # Assume the user has starred the repo

    # Checks the user's 30 most recent starred repos (no cache)
    user_stars = await get_user_stars(user_id)
    return f"{owner}/{repo}" in user_stars


@alru_cache(ttl=timedelta(hours=1))
async def get_is_valid_user(user_id: str) -> Tuple[bool, str]:
    if user_id.lower() in USER_BLACKLIST:
        # TODO: change error message
        return (False, "GitHub user not found")

    if user_id.lower() in USER_WHITELIST:
        return (True, f"Valid user {user_id.lower()}")

    valid_user_id = await check_github_user_exists(user_id)
    if valid_user_id is None:
        return (False, "GitHub user not found")

    valid_db_user = await check_db_user_exists(valid_user_id)
    user_starred = await check_user_starred_repo(valid_user_id)
    if not (user_starred or valid_db_user):
        return (False, "Repo not starred")

    return (True, f"Valid user {valid_user_id}")
