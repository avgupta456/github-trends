from fastapi import APIRouter, Response, status

from src.utils.pubsub import publish_to_topic
from src.utils.decorators import fail_gracefully

router = APIRouter()


@router.get("/pub/user/{user_id}/{access_token}", status_code=status.HTTP_200_OK)
@fail_gracefully
def pub_user(response: Response, user_id: str, access_token: str) -> str:
    publish_to_topic("user", {"user_id": user_id, "access_token": access_token})

    return user_id
