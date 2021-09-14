from datetime import datetime
from typing import Any, Dict, Optional

from src.db.mongodb import USERS
from src.db.models.users import UserModel


async def create_user(user_id: str, access_token: str) -> str:
    user = UserModel.parse_obj(
        {
            "user_id": user_id,
            "access_token": access_token,
            "last_updated": datetime.now(),
            "raw_data": None,
        }
    )
    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": user.dict()},
        upsert=True,
    )
    return user_id


async def update_user(user_id: str, raw_data: Optional[Dict[str, Any]] = None) -> None:
    if raw_data is not None:
        await USERS.update_one(  # type: ignore
            {"user_id": user_id},
            {"$set": {"raw_data": raw_data}},
        )
