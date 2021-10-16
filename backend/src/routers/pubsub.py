from typing import Any, Dict
from datetime import date, timedelta

from fastapi import APIRouter, Response, Request, status

from src.packaging.user import main as get_data
from src.db.functions.users import lock_user, unlock_user, update_user

from src.external.pubsub.templates import publish_to_topic, parse_request
from src.decorators import fail_gracefully, pubsub_fail_gracefully

router = APIRouter()

"""
USER PUBSUB
"""


@router.get("/pub/user/{user_id}/{access_token}", status_code=status.HTTP_200_OK)
@fail_gracefully
def pub_user(response: Response, user_id: str, access_token: str) -> str:
    publish_to_topic("user", {"user_id": user_id, "access_token": access_token})

    return user_id


@router.post("/sub/user/{token}", status_code=status.HTTP_200_OK)
@pubsub_fail_gracefully
async def sub_user(response: Response, token: str, request: Request) -> Any:
    data: Dict[str, Any] = await parse_request(token, request)

    await lock_user(data["user_id"])

    # standard policy is to check past year of data
    start_date = date.today() - timedelta(365)
    end_date = date.today()
    timezone_str = "US/Eastern"

    # TODO: historical data is never updated,
    # don't query full history each time, instead
    # define function to build on previous results

    # TODO: improve performance to store > 1 year
    # ideally five years, leads to issues currently

    output = await get_data(
        data["user_id"],
        data["access_token"],
        start_date,
        end_date,
        timezone_str,
    )

    await update_user(data["user_id"], output)

    await unlock_user(data["user_id"])

    return data
