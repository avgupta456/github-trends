from datetime import date
from fastapi import APIRouter, Response, status

from src.db.secret.functions import get_next_key
from src.helper.alru_cache import alru_cache
from src.packaging.user import main as get_data
from src.models.user.package import UserPackage

from src.decorators import async_fail_gracefully
from src.utils import use_time_range

router = APIRouter()


@alru_cache()
async def get_user_demo(user_id: str) -> UserPackage:
    access_token = await get_next_key("demo")
    start_date, end_date, _ = use_time_range("one_month", date.today(), date.today())
    data = await get_data(user_id, access_token, start_date, end_date)
    return (True, data)  # type: ignore


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user_demo_endpoint(response: Response, user_id: str) -> UserPackage:
    return await get_user_demo(user_id)
