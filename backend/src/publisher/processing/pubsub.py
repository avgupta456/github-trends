from typing import Optional

from src.constants import DOCKER, PROD
from src.subscriber.processing import query_user
from src.utils.pubsub import publish_to_topic


async def publish_user(
    user_id: str,
    access_token: Optional[str] = None,
    private_access: bool = False,
):
    if PROD or DOCKER:
        publish_to_topic(
            topic="user",
            message={
                "user_id": user_id,
                "access_token": access_token,
                "private_access": private_access,
            },
        )
    else:
        return await query_user(user_id, access_token, private_access)
