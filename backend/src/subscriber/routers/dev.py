from datetime import date, timedelta
from typing import Optional, Union

from fastapi import APIRouter, Response, status

from src.data.mongo.secret import update_keys
from src.models import FullUserPackage, UserPackage, WrappedPackage
from src.subscriber.aggregation import (
    get_full_user_data,
    get_user_data,
    get_wrapped_data,
)
from src.utils import async_fail_gracefully, use_time_range

router = APIRouter()


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
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
) -> Union[UserPackage, FullUserPackage]:
    await update_keys()
    start_date, end_date, _ = use_time_range(time_range, start_date, end_date)
    func = get_user_data if not full else get_full_user_data
    data = await func(user_id, start_date, end_date, timezone_str, access_token)
    return data


@router.get("/wrapped/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_wrapped_user_raw(
    response: Response,
    user_id: str,
    access_token: Optional[str] = None,
    year: int = 2021,
) -> WrappedPackage:
    await update_keys()
    data = await get_wrapped_data(user_id, year, access_token)
    return data
