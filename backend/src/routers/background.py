from src.aggregation.layer1 import query_user
from src.models.background import UpdateUserBackgroundTask


async def run_in_background(task: UpdateUserBackgroundTask):
    if isinstance(task, UpdateUserBackgroundTask):  # type: ignore
        await query_user(task.user_id, task.access_token, task.private_access)
