from datetime import datetime
from typing import Any, Dict
from src.constants import OAUTH_CLIENT_ID

from src.data.github.auth import authenticate as github_authenticate
from src.data.mongo.user import (
    update_user,
    delete_user as db_delete_user,
    get_user_by_user_id,
)

from src.utils import publish_to_topic


async def authenticate(code: str, private_access: bool) -> Any:
    user_id, access_token = await github_authenticate(code)
    await login_user(user_id, access_token, private_access)
    return user_id


async def login_user(
    user_id: str, access_token: str, private_access: bool = False
) -> str:
    curr_user = await get_user_by_user_id(user_id)
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
        raw_user["last_updated"] = datetime(1970, 1, 1)

        # triggers data query to fetch private commits
        publish_to_topic("user", {"user_id": user_id, "access_token": access_token})

    if curr_user is None:
        raw_user["last_updated"] = datetime.now()
        raw_user["raw_data"] = None
        raw_user["lock"] = False

    await update_user(user_id, raw_user)

    return user_id


async def delete_user(user_id: str) -> str:
    await db_delete_user(user_id)
    return "https://github.com/settings/connections/applications/" + OAUTH_CLIENT_ID
