from datetime import date, datetime, timedelta
from typing import Optional

from src.data.mongo.user import get_user_by_user_id, UserModel
from src.data.mongo.secret import get_next_key

from src.models import UserPackage

from src.publisher.aggregation import trim_package

# TODO: replace with call to subscriber so compute not on publisher
from src.subscriber.aggregation import get_data

from src.utils import alru_cache
from src.utils.pubsub import publish_to_topic


def validate_raw_data(data: Optional[UserPackage]) -> bool:
    # NOTE: add more validation as more fields are required
    return data is not None and data.contribs is not None


def validate_dt(dt: Optional[datetime], td: timedelta):
    last_updated = dt if dt is not None else datetime(1970, 1, 1)
    time_diff = datetime.now() - last_updated
    return time_diff > timedelta(hours=6)


async def _get_user(user_id: str, no_cache: bool = False) -> Optional[UserPackage]:
    db_user: Optional[UserModel] = await get_user_by_user_id(user_id, no_cache=no_cache)
    if db_user is None or db_user.access_token == "":
        raise LookupError("Invalid UserId")

    valid_dt = validate_dt(db_user.last_updated, timedelta(hours=6))
    if valid_dt or not validate_raw_data(db_user.raw_data):
        if validate_dt(db_user.lock, timedelta(minutes=1)):
            publish_to_topic(
                "user", {"user_id": user_id, "access_token": db_user.access_token}
            )

    if validate_raw_data(db_user.raw_data):
        return db_user.raw_data  # type: ignore

    return None


@alru_cache()
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
