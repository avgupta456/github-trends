from datetime import datetime
from typing import Any, Dict, Optional

from src.db.mongodb import USERS


async def login_user(user_id: str, access_token: str) -> str:
    curr_user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore
    raw_user: Dict[str, Any] = {"user_id": user_id, "access_token": access_token}
    if curr_user is None:
        raw_user["last_updated"] = datetime.now()
        raw_user["raw_data"] = None

    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": raw_user},
        upsert=True,
    )
    return user_id


async def update_user(user_id: str, raw_data: Optional[Dict[str, Any]] = None) -> None:
    if raw_data is not None:
        await USERS.update_one(  # type: ignore
            {"user_id": user_id},
            {"$set": {"last_updated": datetime.now(), "raw_data": raw_data}},
        )
