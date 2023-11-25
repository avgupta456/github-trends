from typing import Any, Dict, Optional, Tuple

from src.data.github.auth import authenticate as github_authenticate
from src.data.mongo.user import (
    PublicUserModel,
    delete_user as db_delete_user,
    get_public_user as db_get_public_user,
    update_user as db_update_user,
)
from src.models.background import UpdateUserBackgroundTask

# frontend first calls set_user_key with code and user_key
# next they call authenticate which determines the user_id to associate with the code/user_key
# these actions should happen sequentially, so in-memory storage is fine
code_key_map: Dict[str, str] = {}


async def set_user_key(code: str, user_key: str) -> str:
    code_key_map[code] = user_key
    return user_key


async def authenticate(
    code: str, private_access: bool
) -> Tuple[str, Optional[UpdateUserBackgroundTask]]:
    user_id, access_token = await github_authenticate(code)

    curr_user: Optional[PublicUserModel] = await db_get_public_user(user_id)

    raw_user: Dict[str, Any] = {
        "user_id": user_id,
        "access_token": access_token,
        "user_key": code_key_map.get(code, None),
        "private_access": private_access,
    }

    background_task = None
    if curr_user is not None:
        curr_private_access = curr_user.private_access
        new_private_access = curr_private_access or private_access
        raw_user["private_access"] = new_private_access

        if new_private_access != curr_private_access:
            # new private access status
            background_task = UpdateUserBackgroundTask(
                user_id=user_id,
                access_token=access_token,
                private_access=new_private_access,
                start_date=None,
                end_date=None,
            )
    else:
        # first time sign up
        background_task = UpdateUserBackgroundTask(
            user_id=user_id,
            access_token=access_token,
            private_access=private_access,
            start_date=None,
            end_date=None,
        )

    await db_update_user(user_id, raw_user)
    return user_id, background_task


async def delete_user(user_id: str, user_key: str, use_user_key: bool = True) -> bool:
    return await db_delete_user(user_id, user_key, use_user_key)
