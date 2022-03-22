from datetime import date, datetime
from typing import Any, Dict, List

from src.constants import API_VERSION
from src.data.mongo.main import USER_MONTHS
from src.data.mongo.user_months.models import UserMonth
from src.models import UserPackage


async def get_user_months(
    user_id: str, start_month: date, end_month: date
) -> List[UserMonth]:
    start = datetime(start_month.year, start_month.month, 1)
    end = datetime(end_month.year, end_month.month, 28)
    months: List[Dict[str, Any]] = await USER_MONTHS.find(  # type: ignore
        {
            "user_id": user_id,
            "month": {"$gte": start, "$lte": end},
            "version": API_VERSION,
            "complete": True,
        }
    ).to_list(length=None)

    months_data: List[UserMonth] = []
    for month in months:
        try:
            data = UserPackage.decompress(month["data"])
            months_data.append(
                UserMonth.parse_obj(
                    {
                        "user_id": user_id,
                        "month": month["month"],
                        "version": API_VERSION,
                        "complete": True,
                        "data": data.dict(),
                    }
                )
            )
        except Exception:
            pass

    return months_data
