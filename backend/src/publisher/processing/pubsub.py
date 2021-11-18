from typing import Optional

from src.utils.pubsub import publish_to_topic


def publish_user(user_id: str, access_token: Optional[str] = None):
    publish_to_topic("user", {"user_id": user_id, "access_token": access_token})


def publish_wrapped_user(user_id: str, year: int, access_token: Optional[str] = None):
    publish_to_topic(
        "wrapped", {"user_id": user_id, "year": year, "access_token": access_token}
    )
