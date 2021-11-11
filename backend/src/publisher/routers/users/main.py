from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Response, status

from src.models import UserPackage
from src.publisher.processing import get_user
from src.publisher.routers.users.db import router as db_router
from src.publisher.routers.users.svg import router as svg_router
from src.publisher.routers.users.wrapped import router as wrapped_router
from src.utils import async_fail_gracefully

router = APIRouter()
router.include_router(db_router, prefix="/db")
router.include_router(svg_router, prefix="/svg")
router.include_router(wrapped_router, prefix="/wrapped")


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
    no_cache: bool = False,
) -> Optional[UserPackage]:
    return await get_user(user_id, start_date, end_date, no_cache=no_cache)
