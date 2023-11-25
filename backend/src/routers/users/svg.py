from datetime import date, timedelta
from typing import Any

from fastapi import BackgroundTasks, Response, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from src.processing.user import get_top_languages, get_top_repos, svg_base
from src.render import (
    get_empty_demo_svg,
    get_loading_svg,
    get_top_langs_svg,
    get_top_repos_svg,
)
from src.routers.background import run_in_background
from src.routers.decorators import svg_fail_gracefully

router = APIRouter()


@router.get(
    "/{user_id}/langs", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_lang_svg(
    response: Response,
    background_tasks: BackgroundTasks,
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
    use_animation: bool = True,
    theme: str = "classic",
) -> Any:
    output, complete, background_task, time_str = await svg_base(
        user_id, start_date, end_date, time_range, demo, no_cache
    )
    if background_task is not None:
        # set a background task to update the user
        background_tasks.add_task(run_in_background, task=background_task)

    # if no data, return loading svg
    if output is None:
        return get_loading_svg()

    # get top languages
    processed, commits_excluded = get_top_languages(output, loc_metric, include_private)
    return get_top_langs_svg(
        data=processed,
        time_str=time_str,
        use_percent=use_percent,
        loc_metric=loc_metric,
        complete=complete,
        commits_excluded=commits_excluded,
        compact=compact,
        use_animation=use_animation,
        theme=theme,
    )


@router.get(
    "/{user_id}/repos", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_repo_svg(
    response: Response,
    background_tasks: BackgroundTasks,
    user_id: str,
    start_date: date = date.today() - timedelta(30),
    end_date: date = date.today(),
    time_range: str = "one_year",
    timezone_str: str = "US/Eastern",
    include_private: bool = False,
    group: str = "none",
    loc_metric: str = "added",
    demo: bool = False,
    no_cache: bool = False,
    use_animation: bool = True,
    theme: str = "classic",
) -> Any:
    output, complete, background_task, time_str = await svg_base(
        user_id, start_date, end_date, time_range, demo, no_cache
    )
    if background_task is not None:
        # set a background task to update the user
        background_tasks.add_task(run_in_background, task=background_task)

    # if no data, return loading svg
    if output is None:
        return get_loading_svg()

    # get top repos
    processed, commits_excluded = get_top_repos(
        output, loc_metric, include_private, group
    )
    return get_top_repos_svg(
        data=processed,
        time_str=time_str,
        loc_metric=loc_metric,
        complete=complete,
        commits_excluded=commits_excluded,
        use_animation=use_animation,
        theme=theme,
    )


@router.get(
    "/demo",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    include_in_schema=False,
)
@svg_fail_gracefully
async def get_demo_svg(response: Response, card: str) -> Any:
    if card == "langs":
        return get_empty_demo_svg("Most Used Languages")
    elif card == "repos":
        return get_empty_demo_svg("Most Contributed Repositories")
    else:
        return get_empty_demo_svg(card)
