from typing import Any, Dict

from src.db.models.users import UserModel

from src.db.mongodb import USERS

"""
Raw Get Methods
"""


async def get_user(user_id: str) -> UserModel:
    user: Dict[str, Any] = await USERS.find_one({"user_id": user_id})  # type: ignore
    return UserModel.parse_obj(user)
