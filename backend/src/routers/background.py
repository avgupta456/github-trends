from typing import Dict

from src.aggregation.layer1 import query_user
from src.models.background import UpdateUserBackgroundTask

# create a cache for the function
cache: Dict[str, Dict[str, bool]] = {"update_user": {}}


async def run_in_background(task: UpdateUserBackgroundTask):
    if isinstance(task, UpdateUserBackgroundTask):  # type: ignore
        inputs = {
            "user_id": task.user_id,
            "access_token": task.access_token,
            "private_access": task.private_access,
            "start_date": task.start_date,
            "end_date": task.end_date,
        }

        inputs = {k: v for k, v in inputs.items() if v is not None}

        # check if the task is already running
        if task.user_id in cache["update_user"]:
            return

        # add the task to the cache
        cache["update_user"][task.user_id] = True

        await query_user(**inputs)  # type: ignore

        # remove the task from the cache
        del cache["update_user"][task.user_id]
