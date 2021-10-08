from datetime import date, timedelta

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
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    time_range: str = "one_month",
    timezone_str: str = "US/Eastern",
) -> UserPackage:
    db_user = await get_user_by_user_id(user_id)
    if db_user is None or db_user.access_token == "":
        raise LookupError("Invalid UserId")

    start_date, end_date, _ = use_time_range(time_range, start_date, end_date)
    data = await get_data(
        user_id, db_user.access_token, start_date, end_date, timezone_str
    )

    return data
