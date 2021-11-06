from datetime import datetime
from typing import Any, Dict, Optional

from src.models import UserPackage

from src.data.mongo.main import USERS
from src.data.mongo.user.compression import compress


async def is_user_key(user_id: str, user_key: str) -> bool:
    user: Optional[dict[str, str]] = await USERS.find_one(  # type: ignore
        {"user_id": user_id}, {"user_key": 1}
    )
    return user is not None and user["user_key"] == user_key


async def lock_user(user_id: str) -> None:
    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": {"lock": datetime.now()}},
    )


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


async def delete_user(user_id: str, user_key: str, use_user_key: bool = True) -> bool:
    if use_user_key and not is_user_key(user_id, user_key):
        return False
    await USERS.delete_one({"user_id": user_id})  # type: ignore
    return True
