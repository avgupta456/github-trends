from typing import Any, Dict, Optional

from src.db.models.users import UserModel

from src.db.mongodb import USERS

"""
Raw Get Methods
"""


async def get_user_by_user_id(user_id: str) -> Optional[UserModel]:
    user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore
    if user is None:
        return None
    return UserModel.parse_obj(user)


async def get_user_by_access_token(access_token: str) -> Optional[UserModel]:
    user: Optional[Dict[str, Any]] = await USERS.find_one(  # type: ignore
        {"access_token": access_token}
    )
    if user is None:
        return None
    return UserModel.parse_obj(user)
