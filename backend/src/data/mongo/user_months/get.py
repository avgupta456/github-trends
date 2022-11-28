from datetime import date, datetime
from typing import Any, Dict, List

from src.constants import API_VERSION
from src.data.mongo.main import USER_MONTHS  # type: ignore
from src.data.mongo.user_months.models import UserMonth
from src.models import UserPackage


async def get_user_months(
    user_id: str, private_access: bool, start_month: date, end_month: date
) -> List[UserMonth]:
    start = datetime(start_month.year, start_month.month, 1)
    end = datetime(end_month.year, end_month.month, 28)
    today = datetime.now()

    filters = {
        "user_id": user_id,
        "month": {"$gte": start, "$lte": end},
        "version": API_VERSION,
    }

    if private_access:
        filters["private"] = True

    months: List[Dict[str, Any]] = await USER_MONTHS.find(filters).to_list(length=None)  # type: ignore

    months_data: List[UserMonth] = []
    for month in months:
        date_obj: datetime = month["month"]
        complete = date_obj.year != today.year or date_obj.month != today.month
        try:
            data = UserPackage.decompress(month["data"])
            months_data.append(
                UserMonth.parse_obj(
                    {
                        "user_id": user_id,
                        "month": month["month"],
                        "version": API_VERSION,
                        "private": month["private"],
                        "complete": complete,
                        "data": data.dict(),
                    }
                )
            )
        except Exception:
            pass

    return months_data
