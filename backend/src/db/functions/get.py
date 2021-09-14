from typing import Any, Dict

from src.db.models.users import UserModel

from src.db.mongodb import USERS

"""
Raw Get Methods
"""


async def get_user_by_user_id(user_id: str) -> UserModel:
    user: Dict[str, Any] = await USERS.find_one({"user_id": user_id})  # type: ignore
    return UserModel.parse_obj(user)


async def get_user_by_access_token(access_token: str) -> UserModel:
    user: Dict[str, Any] = await USERS.find_one({"access_token": access_token})  # type: ignore
    return UserModel.parse_obj(user)
