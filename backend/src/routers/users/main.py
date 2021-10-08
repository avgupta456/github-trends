from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Response, status

from src.models.user.package import UserPackage
from src.utils import async_fail_gracefully
from src.constants import PROD

from src.routers.users.get_data import get_user
from src.routers.users.db import router as db_router
from src.routers.users.svg import router as svg_router
from src.routers.users.dev import router as dev_router

router = APIRouter()
router.include_router(db_router, prefix="/db")
router.include_router(svg_router, prefix="/svg")
if not PROD:
    router.include_router(dev_router, prefix="/dev")


"""
ANALYTICS
"""


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user_endpoint(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Optional[UserPackage]:
    return await get_user(user_id, start_date, end_date)
