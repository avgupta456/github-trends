from datetime import date
from typing import Optional

from src.data.mongo.user import PublicUserModel, get_public_user as db_get_public_user
from src.models import UserPackage, WrappedPackage
from src.subscriber.aggregation import get_wrapped_data
from src.subscriber.processing.user import query_user
from src.utils import alru_cache


@alru_cache()
async def query_wrapped_user(
    user_id: str, year: int, no_cache: bool = False
) -> Optional[WrappedPackage]:
    start_date, end_date = date(year, 1, 1), date(year, 12, 31)
    user: Optional[PublicUserModel] = await db_get_public_user(user_id)
    access_token = None if user is None else user.access_token
    private_access = False if user is None else user.private_access or False
    user_package: Optional[UserPackage] = await query_user(
        user_id, access_token, private_access, start_date, end_date
    )
    if user_package is None:
        return (False, None)  # type: ignore
    wrapped_package = get_wrapped_data(user_package)
    return (True, wrapped_package)  # type: ignore
