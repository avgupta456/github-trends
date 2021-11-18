import requests

from src.data.mongo.secret import update_keys
from src.data.mongo.wrapped import set_wrapped_user
from src.models.wrapped.main import WrappedPackage
from src.subscriber.aggregation import get_wrapped_data
from src.utils.alru_cache import alru_cache

s = requests.Session()


@alru_cache()
async def query_wrapped_user(user_id: str, access_token: str, year: int) -> bool:
    await update_keys()
    wrapped_package: WrappedPackage = await get_wrapped_data(
        user_id=user_id, year=year, access_token=access_token
    )

    await set_wrapped_user(user_id, year, wrapped_package)

    return (True, True)  # type: ignore
