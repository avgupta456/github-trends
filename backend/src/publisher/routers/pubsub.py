from typing import Optional

from fastapi import APIRouter, Response, status

from src.publisher.processing import publish_user
from src.utils import fail_gracefully

router = APIRouter()


@router.get(
    "/pub/user/{user_id}/{access_token}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@fail_gracefully
def pub_user(response: Response, user_id: str, access_token: Optional[str]) -> str:
    publish_user(user_id, access_token)
    return user_id
