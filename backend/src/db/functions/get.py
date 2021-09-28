from typing import Any, Dict, Optional
from datetime import datetime

from src.db.models.users import UserModel

from src.db.mongodb import USERS

"""
Raw Get Methods
"""


async def get_user_by_user_id(user_id: str) -> Optional[UserModel]:
    start = datetime.now()
    user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore
    if user is None:
        return None
    output = UserModel.parse_obj(user)

    print("MongoDB User Query:", datetime.now() - start)
    return output


async def get_user_by_access_token(access_token: str) -> Optional[UserModel]:
    start = datetime.now()
    user: Optional[Dict[str, Any]] = await USERS.find_one(  # type: ignore
        {"access_token": access_token}
    )
    if user is None:
        return None
    output = UserModel.parse_obj(user)

    print("MongoDB User Query:", datetime.now() - start)
    return output
