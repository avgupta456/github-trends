from datetime import date, timedelta
from typing import Any, Optional, Tuple

from fastapi import Response, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from src.analytics.user.commits import get_top_languages, get_top_repos
from src.models.user.package import UserPackage

from src.svg.top_langs import get_top_langs_svg
from src.svg.top_repos import get_top_repos_svg
from src.svg.error import get_loading_svg

from src.helper.decorators import svg_fail_gracefully
from src.helper.utils import use_time_range

from src.routers.users.get_data import get_user, get_user_demo

router = APIRouter()


async def svg_base(
    user_id: str, start_date: date, end_date: date, time_range: str, demo: bool
) -> Tuple[Optional[UserPackage], str]:
    # process time_range, start_date, end_date
    time_range = "one_month" if demo else time_range
    start_date, end_date, time_str = use_time_range(time_range, start_date, end_date)

    # fetch data, either using demo or user method
    if demo:
        output = await get_user_demo(user_id)
    else:
        output = await get_user(user_id, start_date, end_date)

    return output, time_str


@router.get(
    "/{user_id}/langs", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_lang_svg(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(30),
    end_date: date = date.today(),
    time_range: str = "one_year",
    timezone_str: str = "US/Eastern",
    use_percent: bool = False,
    include_private: bool = False,
    loc_metric: str = "added",
    compact: bool = False,
    demo: bool = False,
) -> Any:
    output, time_str = await svg_base(user_id, start_date, end_date, time_range, demo)

    # if no data, return loading svg
    if output is None:
        return get_loading_svg()

    # get top languages
    processed, num_excluded = get_top_languages(output, loc_metric, include_private)
    return get_top_langs_svg(
        processed, time_str, use_percent, loc_metric, num_excluded, compact
    )


@router.get(
    "/{user_id}/repos", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_repo_svg(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(30),
    end_date: date = date.today(),
    time_range: str = "one_year",
    timezone_str: str = "US/Eastern",
    include_private: bool = False,
    loc_metric: str = "added",
    demo: bool = False,
) -> Any:
    output, time_str = await svg_base(user_id, start_date, end_date, time_range, demo)

    # if no data, return loading svg
    if output is None:
        return get_loading_svg()

    # get top repos
    processed, commits_excluded = get_top_repos(output, loc_metric, include_private)
    return get_top_repos_svg(processed, time_str, loc_metric, commits_excluded)
