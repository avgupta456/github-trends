from datetime import timedelta
from typing import List

from src.constants import OWNER, REPO
from src.data.github.rest import get_repo_stargazers as github_get_repo_stargazers
from src.data.github.utils import get_access_token
from src.utils import alru_cache


@alru_cache(ttl=timedelta(minutes=15))
async def get_repo_stargazers(
    owner: str = OWNER, repo: str = REPO, no_cache: bool = False
) -> List[str]:
    access_token = get_access_token()
    data: List[str] = []
    page = 0
    while len(data) == 100 * page:
        temp_data = github_get_repo_stargazers(access_token, owner, repo, page=page)
        temp_data = [x["user"]["login"] for x in temp_data]
        data.extend(temp_data)
        page += 1

    return (True, data)  # type: ignore
