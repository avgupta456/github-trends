from typing import Any, Dict, Optional

from src.data.mongo.main import USERS


async def is_user_key(user_id: str, user_key: str) -> bool:
    user: Optional[dict[str, str]] = await USERS.find_one(
        {"user_id": user_id}, {"user_key": 1}
    )
    return user is not None and user.get("user_key", "") == user_key


async def update_user(user_id: str, raw_user: Dict[str, Any]) -> None:
    await USERS.update_one(
        {"user_id": user_id},
        {"$set": raw_user},
        upsert=True,
    )


async def delete_user(user_id: str, user_key: str, use_user_key: bool = True) -> bool:
    if use_user_key:
        is_key = await is_user_key(user_id, user_key)
        if not is_key:
            return False

    await USERS.delete_one({"user_id": user_id})
    return True
