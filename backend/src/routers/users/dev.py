from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Response, status

from src.db.functions.get import get_user_by_user_id
from src.packaging.user import main as get_data
from src.models.user.package import UserPackage

from src.utils import async_fail_gracefully, use_time_range

router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user_raw(
    response: Response,
    user_id: str,
    access_token: Optional[str] = None,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    time_range: str = "one_month",
    timezone_str: str = "US/Eastern",
) -> UserPackage:
    new_access_token: str = access_token if access_token else ""
    if not access_token:
        db_user = await get_user_by_user_id(user_id, use_cache=False)
        if db_user is None or db_user.access_token == "":
            raise LookupError("Invalid UserId")
        new_access_token = db_user.access_token

    start_date, end_date, _ = use_time_range(time_range, start_date, end_date)
    print(start_date, end_date, user_id, new_access_token, timezone_str)
    data = await get_data(user_id, new_access_token, start_date, end_date, timezone_str)

    return data
