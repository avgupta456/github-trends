from typing import Any, Dict

from fastapi import status
from fastapi.responses import Response
from fastapi.routing import APIRouter

from src.publisher.processing import authenticate, delete_user, set_user_key
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
    response: Response, code: str, private_access: bool = False
) -> str:
    return await authenticate(code, private_access)


@router.get(
    "/delete/{user_id}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    response_model=Dict[str, Any],
)
@async_fail_gracefully
async def delete_user_endpoint(response: Response, user_id: str, user_key: str) -> bool:
    return await delete_user(user_id, user_key=user_key)
