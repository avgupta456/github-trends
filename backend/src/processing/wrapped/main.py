from datetime import date, timedelta
from typing import Optional, Tuple

from src.aggregation.layer1 import query_user
from src.data.mongo.user import PublicUserModel, get_public_user as db_get_public_user
from src.models import UserPackage, WrappedPackage
from src.processing.wrapped.package import get_wrapped_data
from src.utils import alru_cache


@alru_cache(ttl=timedelta(hours=12))
async def query_wrapped_user(
    user_id: str, year: int, no_cache: bool = False
) -> Tuple[bool, Optional[WrappedPackage]]:
    start_date, end_date = date(year, 1, 1), date(year, 12, 31)
    user: Optional[PublicUserModel] = await db_get_public_user(user_id)
    access_token = None if user is None else user.access_token
    private_access = False if user is None else user.private_access or False
    user_package: UserPackage = await query_user(
        user_id,
        access_token,
        private_access,
        start_date,
        end_date,
        max_time=40,
        no_cache=True,
    )
    wrapped_package = get_wrapped_data(user_package, year)

    # Don't cache if incomplete
    return (not wrapped_package.incomplete, wrapped_package)
