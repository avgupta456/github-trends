from datetime import date, datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, Response, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from src.db.models.users import UserModel as DBUserModel
from src.db.functions.users import login_user
from src.db.functions.get import get_user_by_user_id

from src.constants import PUBSUB_PUB
from src.external.pubsub.templates import publish_to_topic
from src.svg.top_langs import get_top_langs_svg
from src.svg.error import get_loading_svg
from src.utils import async_fail_gracefully, svg_fail_gracefully

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


def validate_raw_data(data: Optional[Dict[str, Any]]) -> bool:
    # NOTE: add more validation as more fields are required
    return data is not None and "top_languages" in data


async def _get_user(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Dict[str, Any]:
    if not PUBSUB_PUB:
        raise HTTPException(400, "")

    db_user = await get_user_by_user_id(user_id)
    if db_user is None or db_user.access_token == "":
        raise LookupError("Invalid UserId")

    time_diff = datetime.now() - db_user.last_updated
    if time_diff > timedelta(hours=6) or not validate_raw_data(db_user.raw_data):
        if not db_user.lock:
            publish_to_topic(
                "user",
                {
                    "user_id": user_id,
                    "access_token": db_user.access_token,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "timezone_str": timezone_str,
                },
            )

    if validate_raw_data(db_user.raw_data):
        return db_user.raw_data  # type: ignore

    return {}


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Dict[str, Any]:
    return await _get_user(user_id, start_date, end_date, timezone_str)


@router.get(
    "/{user_id}/svg", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_svg(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Any:
    output = await _get_user(user_id, start_date, end_date, timezone_str)
    if not validate_raw_data(output):
        return get_loading_svg()
    return get_top_langs_svg(output)
