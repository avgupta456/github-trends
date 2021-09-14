from typing import Optional

from fastapi import APIRouter, Response, status

from src.utils import async_fail_gracefully

from src.db.models.users import UserModel as DBUserModel
from src.db.functions.users import create_user
from src.db.functions.get import get_user

router = APIRouter()


@router.get("/create/{user_id}/{access_token}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def create_user_endpoint(
    response: Response, user_id: str, access_token: str
) -> str:
    return await create_user(user_id, access_token)


@router.get("/user/get/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user_endpoint(response: Response, user_id: str) -> Optional[DBUserModel]:
    return await get_user(user_id)
