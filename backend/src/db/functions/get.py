from typing import Any, Dict, Optional

from src.db.mongodb import USERS
from src.db.functions.compression import decompress
from src.db.models.users import UserModel


"""
Raw Get Methods
"""


def _get_user(user: Optional[Dict[str, Any]]) -> Optional[UserModel]:
    if user is None:
        return None

    if "raw_data" not in user:
        return UserModel.parse_obj(user)

    raw_data = decompress(user["raw_data"])
    return UserModel.parse_obj({**user, "raw_data": raw_data})


async def get_user_by_user_id(user_id: str) -> Optional[UserModel]:
    user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore
    output = _get_user(user)
    return output


async def get_user_by_access_token(access_token: str) -> Optional[UserModel]:
    user: Optional[Dict[str, Any]] = await USERS.find_one(  # type: ignore
        {"access_token": access_token}
    )
    output = _get_user(user)
    return output
