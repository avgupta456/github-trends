from typing import Any, Dict

from fastapi import BackgroundTasks, status
from fastapi.responses import Response
from fastapi.routing import APIRouter

from src.processing.auth import authenticate, delete_user, set_user_key
from src.routers.background import run_in_background
from src.utils import async_fail_gracefully

router = APIRouter()


@router.post(
    "/set_user_key/{code}/{user_key}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    response_model=Dict[str, Any],
)
@async_fail_gracefully
async def set_user_key_endpoint(response: Response, code: str, user_key: str) -> str:
    return await set_user_key(code, user_key)


@router.post(
    "/login/{code}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    response_model=Dict[str, Any],
)
@async_fail_gracefully
async def authenticate_endpoint(
    response: Response,
    background_tasks: BackgroundTasks,
    code: str,
    private_access: bool = False,
) -> str:
    output, background_task = await authenticate(code, private_access)
    if background_task is not None:
        # set a background task to update the user
        background_tasks.add_task(run_in_background, task=background_task)
    return output


@router.get(
    "/delete/{user_id}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    response_model=Dict[str, Any],
)
@async_fail_gracefully
async def delete_user_endpoint(response: Response, user_id: str, user_key: str) -> bool:
    return await delete_user(user_id, user_key=user_key)
