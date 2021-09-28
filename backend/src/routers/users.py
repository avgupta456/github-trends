from datetime import date, datetime, timedelta
from typing import Any, Optional

from fastapi import APIRouter, Response, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from src.db.models.users import UserModel as DBUserModel
from src.db.functions.users import login_user
from src.db.functions.get import get_user_by_user_id

from src.external.pubsub.templates import publish_to_topic
from src.models.user.package import UserPackage

from src.analytics.user.utils import trim_package
from src.analytics.user.commits import get_top_languages, get_top_repos

from src.svg.top_langs import get_top_langs_svg
from src.svg.top_repos import get_top_repos_svg
from src.svg.error import get_loading_svg

from src.constants import PUBSUB_PUB
from src.utils import async_fail_gracefully, svg_fail_gracefully  # , alru_cache

router = APIRouter()


"""
DATABASE SECTION
"""


@router.get("/db/create/{user_id}/{access_token}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def create_user_endpoint(
    response: Response, user_id: str, access_token: str
) -> str:
    return await login_user(user_id, access_token)


@router.get("/db/get/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user_endpoint(response: Response, user_id: str) -> Optional[DBUserModel]:
    return await get_user_by_user_id(user_id)


"""
ANALYTICS/SVG SECTION
"""


def validate_raw_data(data: Optional[UserPackage]) -> bool:
    # NOTE: add more validation as more fields are required
    return data is not None and data.contribs is not None


# TODO: add cache to this endpoint
# @alru_cache(ttl=timedelta(minutes=5))
async def __get_user(user_id: str) -> Optional[UserPackage]:
    if not PUBSUB_PUB:
        raise HTTPException(400, "")

    db_user = await get_user_by_user_id(user_id)
    if db_user is None or db_user.access_token == "":
        raise LookupError("Invalid UserId")

    time_diff = datetime.now() - db_user.last_updated
    if time_diff > timedelta(hours=6) or not validate_raw_data(db_user.raw_data):
        if not db_user.lock:
            publish_to_topic(
                "user", {"user_id": user_id, "access_token": db_user.access_token}
            )

    if validate_raw_data(db_user.raw_data):
        return db_user.raw_data  # type: ignore

    return None


async def _get_user(
    user_id: str, start_date: date, end_date: date
) -> Optional[UserPackage]:
    output = await __get_user(user_id)

    if output is None:
        return None

    output = trim_package(output, start_date, end_date)

    # TODO: handle timezone_str here

    return output


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Optional[UserPackage]:
    return await _get_user(user_id, start_date, end_date)


@router.get(
    "/{user_id}/svg/langs", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_lang_svg(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
    use_percent: bool = True,
) -> Any:
    output = await _get_user(user_id, start_date, end_date)
    if output is None:
        return get_loading_svg()
    processed = get_top_languages(output)
    return get_top_langs_svg(processed, use_percent)


@router.get(
    "/{user_id}/svg/repos", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_repo_svg(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Any:
    output = await _get_user(user_id, start_date, end_date)
    if output is None:
        return get_loading_svg()
    processed = get_top_repos(output)
    return get_top_repos_svg(processed)
