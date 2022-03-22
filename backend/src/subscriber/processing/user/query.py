from calendar import monthrange
from datetime import date, timedelta
from typing import List, Optional

import requests

from src.constants import API_VERSION
from src.data.mongo.secret import update_keys
from src.data.mongo.user import lock_user, update_user_last_access
from src.data.mongo.user_months import get_user_months, set_user_month, UserMonth
from src.models import UserPackage
from src.subscriber.aggregation import get_user_data
from src.utils import alru_cache, date_to_datetime

s = requests.Session()

# NOTE: query user from PubSub, not from subscriber user router


async def query_user_month(user_id: str, start_date: date, access_token: Optional[str]):
    year, month = start_date.year, start_date.month
    end_day = monthrange(year, month)[1]
    end_date = date(year, month, end_day)

    data = await get_user_data(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        timezone_str="US/Eastern",
        access_token=access_token,
    )

    user_month = UserMonth.parse_obj(
        {
            "user_id": user_id,
            "month": date_to_datetime(start_date),
            "version": API_VERSION,
            "complete": True,  # TODO: revisit
            "data": data,
        }
    )

    await set_user_month(user_month)

    return data


@alru_cache()
async def query_user(user_id: str, access_token: Optional[str]) -> bool:
    await update_keys()
    await lock_user(user_id)

    start_date = date.today() - timedelta(365)
    end_date = date.today()

    curr_data: List[UserMonth] = await get_user_months(user_id, start_date, end_date)
    curr_months = [x.month for x in curr_data]

    month, year = start_date.month, start_date.year
    months: List[date] = []
    while date(year, month, 1) <= end_date:
        start = date(year, month, 1)
        if date_to_datetime(start) not in curr_months:
            months.append(start)
        month = month % 12 + 1
        year = year + (month == 1)

    user_packages: List[UserPackage] = []
    for month in months:
        data = await query_user_month(user_id, month, access_token)
        user_packages.append(data)

    await update_user_last_access(user_id)

    return (True, True)  # type: ignore
