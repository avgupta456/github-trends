from datetime import date, timedelta
from typing import Any, Optional, Tuple

from fastapi import Response, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from src.models import UserPackage

from src.publisher.aggregation import get_top_languages, get_top_repos

from src.publisher.render import (
    get_top_langs_svg,
    get_top_repos_svg,
    get_empty_demo_svg,
    get_loading_svg,
)

from src.publisher.processing import get_user, get_user_demo
from src.publisher.routers.decorators import svg_fail_gracefully

from src.utils import use_time_range

router = APIRouter()


async def svg_base(
    user_id: str,
    start_date: date,
    end_date: date,
    time_range: str,
    demo: bool,
    no_cache: bool = False,
) -> Tuple[Optional[UserPackage], str]:
    # process time_range, start_date, end_date
    time_range = "one_month" if demo else time_range
    start_date, end_date, time_str = use_time_range(time_range, start_date, end_date)

    # fetch data, either using demo or user method
    if demo:
        output = await get_user_demo(user_id, start_date, end_date, no_cache=no_cache)
    else:
        output = await get_user(user_id, start_date, end_date, no_cache=no_cache)

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
    no_cache: bool = False,
) -> Any:
    output, time_str = await svg_base(
        user_id, start_date, end_date, time_range, demo, no_cache
    )

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
    no_cache: bool = False,
) -> Any:
    output, time_str = await svg_base(
        user_id, start_date, end_date, time_range, demo, no_cache
    )

    # if no data, return loading svg
    if output is None:
        return get_loading_svg()

    # get top repos
    processed, commits_excluded = get_top_repos(output, loc_metric, include_private)
    return get_top_repos_svg(processed, time_str, loc_metric, commits_excluded)


@router.get("/demo", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
@svg_fail_gracefully
async def get_demo_svg(response: Response, card: str) -> Any:
    if card == "langs":
        return get_empty_demo_svg("Most Used Languages")
    elif card == "repos":
        return get_empty_demo_svg("Most Contributed Repositories")
    else:
        return get_empty_demo_svg(card)