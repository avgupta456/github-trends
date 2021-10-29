from datetime import datetime, date
from typing import Any, Dict, Optional
from src.external.pubsub.templates import publish_to_topic

from src.models.user.package import UserPackage
from src.db.mongodb import USERS
from src.db.user.compression import compress
from src.helper.utils import date_to_datetime


async def login_user(
    user_id: str, access_token: str, private_access: bool = False
) -> str:
    curr_user: Optional[Dict[str, Any]] = await USERS.find_one({"user_id": user_id})  # type: ignore
    raw_user: Dict[str, Any] = {
        "user_id": user_id,
        "access_token": access_token,
    }

    # update private access without downgrading
    curr_private_access = curr_user.get("private_access", False) if curr_user else False
    new_private_access = curr_private_access or private_access

    raw_user["private_access"] = new_private_access
    if new_private_access != curr_private_access:
        # queues data query after cache expires
        raw_user["last_updated"] = date_to_datetime(date(1970, 1, 1))

        # triggers data query to fetch private commits
        publish_to_topic("user", {"user_id": user_id, "access_token": access_token})

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
        {"$set": {"lock": datetime.now()}},
    )


async def update_user(user_id: str, raw_data: Optional[UserPackage] = None) -> None:
    if raw_data is not None:
        compressed_data = compress(raw_data.dict())
        await USERS.update_one(  # type: ignore
            {"user_id": user_id},
            {"$set": {"last_updated": datetime.now(), "raw_data": compressed_data}},
        )


async def delete_user(user_id: str) -> bool:
    result: Any = await USERS.delete_one({"user_id": user_id})  # type: ignore
    print(user_id, result)
    return True
