from typing import Any, Dict
from datetime import date, timedelta, datetime

from fastapi import APIRouter, Response, Request, status

from src.analytics.user.main import get_user as analytics_get_user
from src.db.functions.users import lock_user, unlock_user, update_user

from src.external.pubsub.templates import publish_to_topic, parse_request
from src.utils import fail_gracefully, pubsub_fail_gracefully

router = APIRouter()

"""
USER PUBSUB
"""


@router.get("/pub/user/{user_id}/{access_token}", status_code=status.HTTP_200_OK)
@fail_gracefully
def pub_user(response: Response, user_id: str, access_token: str) -> str:
    publish_to_topic(
        "user",
        {
            "user_id": user_id,
            "access_token": access_token,
            "start_date": str(date.today() - timedelta(365)),
            "end_date": str(date.today()),
            "timezone_str": "US/Eastern",
        },
    )

    return user_id


@router.post("/sub/user/{token}", status_code=status.HTTP_200_OK)
@pubsub_fail_gracefully
async def sub_user(response: Response, token: str, request: Request) -> Any:
    data: Dict[str, Any] = await parse_request(token, request)

    await lock_user(data["user_id"])

    output = await analytics_get_user(
        data["user_id"],
        data["access_token"],
        datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
        datetime.strptime(data["end_date"], "%Y-%m-%d").date(),
        data["timezone_str"],
    )

    await update_user(data["user_id"], output)

    await unlock_user(data["user_id"])

    return output
