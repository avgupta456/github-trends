from datetime import date

import requests

from src.data.mongo.wrapped import set_wrapped_user
from src.models.wrapped.main import WrappedPackage
from src.subscriber.aggregation import get_data
from src.utils.alru_cache import alru_cache

s = requests.Session()


@alru_cache()
async def query_wrapped_user(user_id: str, access_token: str, year: int) -> bool:
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    timezone_str = "US/Eastern"

    user_package = await get_data(
        user_id, access_token, start_date, end_date, timezone_str
    )

    wrapped_package = WrappedPackage.parse_obj({"data": user_package.dict()})

    await set_wrapped_user(user_id, year, wrapped_package)

    return (True, True)  # type: ignore
