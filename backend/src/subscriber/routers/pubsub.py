from typing import Any, Dict

from fastapi import APIRouter, Response, Request, status

from src.subscriber.processing import query_user

from src.subscriber.routers.decorators import pubsub_fail_gracefully

from src.utils.pubsub import parse_request

router = APIRouter()

"""
USER PUBSUB
"""


@router.post("/sub/user/{token}", status_code=status.HTTP_200_OK)
@pubsub_fail_gracefully
async def sub_user(response: Response, token: str, request: Request) -> Any:
    data: Dict[str, Any] = await parse_request(token, request)
    await query_user(data["user_id"], data["access_token"])
    return data
