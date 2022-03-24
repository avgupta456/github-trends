from typing import Optional

from src.utils.pubsub import publish_to_topic


def publish_user(
    user_id: str,
    access_token: Optional[str] = None,
    private_access: bool = False,
):
    publish_to_topic(
        "user",
        {
            "user_id": user_id,
            "access_token": access_token,
            "private_access": private_access,
        },
    )
