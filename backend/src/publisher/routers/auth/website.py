from fastapi import status
from fastapi.routing import APIRouter
from fastapi.responses import Response

from src.publisher.processing import set_user_key, authenticate
from src.utils import async_fail_gracefully


router = APIRouter()


@router.post(
    "/set_user_key/{code}/{user_key}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@async_fail_gracefully
async def set_user_key_endpoint(response: Response, code: str, user_key: str) -> str:
    return await set_user_key(code, user_key)


@router.post("/login/{code}", status_code=status.HTTP_200_OK, include_in_schema=False)
@async_fail_gracefully
async def authenticate_endpoint(
    response: Response, code: str, private_access: bool = False
) -> str:
    return await authenticate(code, private_access)
