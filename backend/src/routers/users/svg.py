from datetime import date, timedelta
from typing import Any

from fastapi import Response, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from src.analytics.user.commits import get_top_languages, get_top_repos

from src.svg.top_langs import get_top_langs_svg
from src.svg.top_repos import get_top_repos_svg
from src.svg.error import get_loading_svg

from src.utils import svg_fail_gracefully, use_time_range

from src.routers.users.get_data import get_user

router = APIRouter()


@router.get(
    "/{user_id}/langs", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_lang_svg(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    time_range: str = "one_year",
    timezone_str: str = "US/Eastern",
    use_percent: bool = False,
    include_private: bool = False,
) -> Any:
    start_date, end_date, time_str = use_time_range(time_range, start_date, end_date)
    output = await get_user(user_id, start_date, end_date)
    if output is None:
        return get_loading_svg()
    processed, commits_excluded = get_top_languages(output, include_private)
    out = get_top_langs_svg(processed, time_str, use_percent, commits_excluded)
    return out


@router.get(
    "/{user_id}/repos", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_repo_svg(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    time_range: str = "one_year",
    timezone_str: str = "US/Eastern",
    include_private: bool = False,
) -> Any:
    start_date, end_date, time_str = use_time_range(time_range, start_date, end_date)
    output = await get_user(user_id, start_date, end_date)
    if output is None:
        return get_loading_svg()
    processed, commits_excluded = get_top_repos(output, include_private)
    return get_top_repos_svg(processed, time_str, commits_excluded)
