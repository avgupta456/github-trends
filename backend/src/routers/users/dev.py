from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Response, status

from src.db.user.get import get_user_by_user_id
from src.db.user.models import UserModel
from src.external.github_api.graphql.template import get_query_limit
from src.packaging.user import main as get_data
from src.models.user.package import UserPackage

from src.helper.decorators import async_fail_gracefully
from src.helper.utils import use_time_range

router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user_raw(
    response: Response,
    user_id: str,
    access_token: Optional[str] = None,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    time_range: str = "one_month",
    timezone_str: str = "US/Eastern",
) -> UserPackage:
    new_access_token: str = access_token if access_token else ""
    if not access_token:
        db_user: UserModel = await get_user_by_user_id(user_id, no_cache=True)
        if db_user is None or db_user.access_token == "":
            raise LookupError("Invalid UserId")
        new_access_token = db_user.access_token

    start_query_limit = get_query_limit(access_token=new_access_token)
    start_date, end_date, _ = use_time_range(time_range, start_date, end_date)
    data = await get_data(user_id, new_access_token, start_date, end_date, timezone_str)
    end_query_limit = get_query_limit(access_token=new_access_token)
    print("Query Limit Used", start_query_limit - end_query_limit)
    print("Query Limit Remaining", end_query_limit)

    return data
