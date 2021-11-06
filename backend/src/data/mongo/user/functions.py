from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from src.models import UserPackage

from src.data.mongo.main import USERS
from src.data.mongo.user.compression import compress


async def lock_user(user_id: str) -> None:
    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": {"lock": datetime.now()}},
    )


async def is_user_locked(user_id: str) -> bool:
    """Returns true if user is locked, false otherwise"""
    user = await USERS.find_one({"user_id": user_id}, {"lock": 1})  # type: ignore
    last_updated: datetime = datetime(1970, 1, 1)
    if user is not None and user["lock"] is not None:
        last_updated: datetime = user["lock"]
    time_diff = datetime.now() - last_updated
    return time_diff < timedelta(minutes=1)


async def update_user_metadata(user_id: str, raw_user: Dict[str, Any]) -> None:
    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": raw_user},
        upsert=True,
    )


async def update_user_raw_data(
    user_id: str, raw_data: Optional[UserPackage] = None
) -> None:
    if raw_data is not None:
        compressed_data = compress(raw_data.dict())
        await USERS.update_one(  # type: ignore
            {"user_id": user_id},
            {"$set": {"last_updated": datetime.now(), "raw_data": compressed_data}},
        )


async def delete_user(user_id: str) -> None:
    await USERS.delete_one({"user_id": user_id})  # type: ignore
