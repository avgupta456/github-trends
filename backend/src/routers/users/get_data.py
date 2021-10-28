from datetime import date, datetime, timedelta
from typing import Optional

from fastapi.exceptions import HTTPException

from src.db.user.get import get_user_by_user_id
from src.db.secret.functions import get_next_key
from src.db.user.models import UserModel

from src.external.pubsub.templates import publish_to_topic
from src.models.user.package import UserPackage

from src.packaging.user import main as get_data
from src.analytics.user.utils import trim_package

from src.helper.alru_cache import alru_cache
from src.constants import PUBSUB_PUB


def validate_raw_data(data: Optional[UserPackage]) -> bool:
    # NOTE: add more validation as more fields are required
    return data is not None and data.contribs is not None


async def _get_user(user_id: str, no_cache: bool = False) -> Optional[UserPackage]:
    if not PUBSUB_PUB:
        raise HTTPException(400, "")

    db_user: Optional[UserModel] = await get_user_by_user_id(user_id, no_cache=no_cache)
    if db_user is None or db_user.access_token == "":
        raise LookupError("Invalid UserId")

    last_updated: datetime = datetime(1970, 1, 1)
    if db_user.last_updated is not None:
        last_updated = db_user.last_updated

    time_diff = datetime.now() - last_updated
    if time_diff > timedelta(hours=6) or not validate_raw_data(db_user.raw_data):
        if db_user.lock is None or not db_user.lock:
            publish_to_topic(
                "user", {"user_id": user_id, "access_token": db_user.access_token}
            )

    if validate_raw_data(db_user.raw_data):
        return db_user.raw_data  # type: ignore

    return None


@alru_cache(max_size=128)
async def get_user(
    user_id: str,
    start_date: date,
    end_date: date,
    no_cache: bool = False,
) -> Optional[UserPackage]:
    output = await _get_user(user_id, no_cache=no_cache)

    if output is None:
        return (False, None)  # type: ignore

    output = trim_package(output, start_date, end_date)

    # TODO: handle timezone_str here

    return (True, output)  # type: ignore


@alru_cache()
async def get_user_demo(
    user_id: str, start_date: date, end_date: date, no_cache: bool = False
) -> UserPackage:
    access_token = await get_next_key("demo", no_cache=no_cache)
    data = await get_data(user_id, access_token, start_date, end_date)
    return (True, data)  # type: ignore
