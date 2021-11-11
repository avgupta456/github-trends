from src.utils.pubsub import publish_to_topic


def publish_user(user_id: str, access_token: str):
    publish_to_topic("user", {"user_id": user_id, "access_token": access_token})


def publish_wrapped_user(user_id: str, access_token: str, year: int):
    publish_to_topic(
        "wrapped", {"user_id": user_id, "access_token": access_token, "year": year}
    )
