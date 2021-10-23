from datetime import datetime
from typing import Any, Dict, Optional

from src.models.user.package import UserPackage
from src.db.mongodb import USERS
from src.db.user.compression import compress


async def login_user(user_id: str, access_token: str) -> str:
    curr_user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore
    raw_user: Dict[str, Any] = {"user_id": user_id, "access_token": access_token}

    if curr_user is None:
        raw_user["last_updated"] = datetime.now()
        raw_user["raw_data"] = None
        raw_user["lock"] = False

    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": raw_user},
        upsert=True,
    )

    return user_id


async def lock_user(user_id: str) -> None:
    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": {"lock": True}},
    )


async def unlock_user(user_id: str) -> None:
    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": {"lock": False}},
    )


async def update_user(user_id: str, raw_data: Optional[UserPackage] = None) -> None:
    if raw_data is not None:
        compressed_data = compress(raw_data.dict())
        await USERS.update_one(  # type: ignore
            {"user_id": user_id},
            {"$set": {"last_updated": datetime.now(), "raw_data": compressed_data}},
        )
