from datetime import date, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, Response, status

from src.aggregation.layer0 import get_user_data
from src.data.mongo.secret import update_keys
from src.models import UserPackage, WrappedPackage
from src.processing.wrapped.package import get_wrapped_data
from src.utils import async_fail_gracefully, use_time_range

router = APIRouter()


@router.get(
    "/user/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any]
)
@async_fail_gracefully
async def get_user_raw(
    response: Response,
    user_id: str,
    access_token: Optional[str] = None,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    time_range: str = "one_month",
    timezone_str: str = "US/Eastern",
    full: bool = False,
) -> UserPackage:
    await update_keys()
    start_date, end_date, _ = use_time_range(time_range, start_date, end_date)
    return await get_user_data(
        user_id, start_date, end_date, timezone_str, access_token
    )


@router.get(
    "/wrapped/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any]
)
@async_fail_gracefully
async def get_wrapped_user_raw(
    response: Response,
    user_id: str,
    year: int = 2024,
    access_token: Optional[str] = None,
) -> WrappedPackage:
    await update_keys()
    user_data = await get_user_data(
        user_id, date(year, 1, 1), date(year, 12, 31), "US/Eastern", access_token
    )
    return get_wrapped_data(user_data, year)
