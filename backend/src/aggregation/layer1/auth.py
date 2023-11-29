from datetime import timedelta
from typing import List, Optional, Tuple

from src.constants import OWNER, REPO
from src.data.github.rest import (
    RESTError,
    RESTErrorNotFound,
    get_repo_stargazers as github_get_repo_stargazers,
    get_user as github_get_user,
    get_user_starred_repos as github_get_user_starred_repos,
)
from src.data.github.utils import get_access_token
from src.data.mongo.user import get_public_user as db_get_public_user
from src.utils import alru_cache


async def get_valid_github_user(user_id: str) -> Optional[str]:
    access_token = get_access_token()
    try:
        return github_get_user(user_id, access_token)["login"]
    except (RESTErrorNotFound, KeyError):
        # User does not exist
        return None
    except RESTError:
        # Rate limited, so assume user exists
        return user_id


async def get_valid_db_user(user_id: str) -> bool:
    user = await db_get_public_user(user_id)
    return user is not None


@alru_cache(ttl=timedelta(minutes=15))
async def get_repo_stargazers(
    owner: str = OWNER, repo: str = REPO, no_cache: bool = False
) -> Tuple[bool, List[str]]:
    access_token = get_access_token()
    data: List[str] = []
    page = 0
    while len(data) == 100 * page:
        temp_data = github_get_repo_stargazers(access_token, owner, repo, page=page)
        temp_data = [x["user"]["login"] for x in temp_data]
        data.extend(temp_data)
        page += 1

    return (True, data)


async def get_user_stars(user_id: str) -> List[str]:
    access_token = get_access_token()
    try:
        data = github_get_user_starred_repos(user_id, access_token)
        data = [x["repo"]["full_name"] for x in data]
        return data
    except RESTErrorNotFound:
        # User does not exist (and rate limited previously)
        return []
    except RESTError:
        # Rate limited, so assume user starred repo
        return [f"{OWNER}/{REPO}"]
