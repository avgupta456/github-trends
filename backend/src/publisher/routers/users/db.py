from typing import Optional

from fastapi import APIRouter, Response, status

from src.data.mongo.user.models import UserMetadata, UserModel
from src.data.mongo.user.get import get_user_by_user_id, get_user_metadata

from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/get/metadata/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_db_user_metadata(
    response: Response, user_id: str, no_cache: bool = False
) -> Optional[UserMetadata]:
    return await get_user_metadata(user_id, no_cache=no_cache)


@router.get("/get/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_db_user(
    response: Response, user_id: str, no_cache: bool = False
) -> Optional[UserModel]:
    return await get_user_by_user_id(user_id, no_cache=no_cache)
