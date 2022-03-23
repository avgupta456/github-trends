from calendar import monthrange
from datetime import date, datetime, timedelta
from typing import List, Optional

import requests

from src.constants import API_VERSION
from src.data.mongo.secret import update_keys
from src.data.mongo.user_months import UserMonth, get_user_months, set_user_month
from src.subscriber.aggregation import get_user_data
from src.utils import alru_cache, date_to_datetime

s = requests.Session()

# NOTE: query user from PubSub, not from subscriber user router


async def query_user_month(
    user_id: str, start_date: date, access_token: Optional[str]
) -> bool:
    year, month = start_date.year, start_date.month
    end_day = monthrange(year, month)[1]
    end_date = date(year, month, end_day)

    try:
        data = await get_user_data(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            timezone_str="US/Eastern",
            access_token=access_token,
        )
    except Exception as e:
        print("Failed to get user data", user_id, start_date, end_date)
        print(e)
        print()

        return False

    month_completed = datetime.now() > date_to_datetime(end_date) + timedelta(days=1)
    user_month = UserMonth.parse_obj(
        {
            "user_id": user_id,
            "month": date_to_datetime(start_date),
            "version": API_VERSION,
            "complete": month_completed,
            "data": data,
        }
    )

    await set_user_month(user_month)

    return True


@alru_cache()
async def query_user(user_id: str, access_token: Optional[str]) -> bool:
    await update_keys()

    start_date = date.today() - timedelta(365)
    end_date = date.today()

    curr_data: List[UserMonth] = await get_user_months(user_id, start_date, end_date)
    curr_months = [x.month for x in curr_data if x.complete]

    month, year = start_date.month, start_date.year
    months: List[date] = []
    while date(year, month, 1) <= end_date:
        start = date(year, month, 1)
        if date_to_datetime(start) not in curr_months:
            months.append(start)
        month = month % 12 + 1
        year = year + (month == 1)

    success = True
    for month in months:
        status = await query_user_month(user_id, month, access_token)
        success = success and status

    # only cache if successful
    return (success, success)  # type: ignore
