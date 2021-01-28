from datetime import date, timedelta

from processing.user.contributions import get_contributions
from processing.user.follows import get_user_follows

from models.user.package import UserPackage

from helper.gather import gather


def main(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> UserPackage:
    """packages all processing steps for the user query"""
    data = gather(
        funcs=[get_contributions, get_user_follows],
        args_dicts=[
            {
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date,
                "timezone_str": timezone_str,
            },
            {"user_id": user_id},
        ],
    )

    return UserPackage(contribs=data[0], follows=data[1])
