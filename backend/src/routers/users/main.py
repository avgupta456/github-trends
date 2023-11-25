from datetime import date, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, BackgroundTasks, Response, status

from src.aggregation.layer2 import get_user
from src.models import UserPackage
from src.routers.background import run_in_background
from src.routers.users.db import router as db_router
from src.routers.users.svg import router as svg_router
from src.utils import async_fail_gracefully

router = APIRouter()
router.include_router(db_router, prefix="/db")
router.include_router(svg_router, prefix="/svg")


"""
ANALYTICS
"""


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
@async_fail_gracefully
async def get_user_endpoint(
    response: Response,
    background_tasks: BackgroundTasks,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
    no_cache: bool = False,
) -> Optional[UserPackage]:
    output, _, background_task = await get_user(
        user_id, start_date, end_date, no_cache=no_cache
    )
    if background_task is not None:
        # set a background task to update the user
        background_tasks.add_task(run_in_background, task=background_task)

    return output
