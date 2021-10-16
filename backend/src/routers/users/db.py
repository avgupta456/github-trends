from typing import Optional

from fastapi import APIRouter, Response, status

from src.db.models.users import UserModel as DBUserModel
from src.db.functions.users import login_user
from src.db.functions.get import get_user_by_user_id

from src.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/create/{user_id}/{access_token}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def create_db_user(response: Response, user_id: str, access_token: str) -> str:
    return await login_user(user_id, access_token)


@router.get("/get/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_db_user(response: Response, user_id: str) -> Optional[DBUserModel]:
    return await get_user_by_user_id(user_id)
