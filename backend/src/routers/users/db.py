from typing import Any, Dict, Optional

from fastapi import APIRouter, Response, status

from src.data.mongo.user import PublicUserModel, get_public_user as db_get_public_user
from src.utils import async_fail_gracefully

router = APIRouter()


@router.get(
    "/get/metadata/{user_id}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    response_model=Dict[str, Any],
)
@async_fail_gracefully
async def get_db_public_user(
    response: Response, user_id: str, no_cache: bool = False
) -> Optional[PublicUserModel]:
    return await db_get_public_user(user_id, no_cache=no_cache)


"""
@router.get("/get/{user_id}", status_code=status.HTTP_200_OK, include_in_schema=False)
@async_fail_gracefully
async def get_db_user(
    response: Response, user_id: str, no_cache: bool = False
) -> Optional[ExternalUserModel]:
    user: Optional[UserModel] = await get_user_by_user_id(user_id, no_cache=no_cache)
    if user is None:
        return None
    return ExternalUserModel.parse_obj(user.dict())
"""
