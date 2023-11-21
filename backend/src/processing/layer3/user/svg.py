from datetime import date
from typing import Optional, Tuple

from src.models import UserPackage
from src.processing.layer3.user.get_data import get_user, get_user_demo
from src.utils import use_time_range


async def svg_base(
    user_id: str,
    start_date: date,
    end_date: date,
    time_range: str,
    demo: bool,
    no_cache: bool = False,
) -> Tuple[Optional[UserPackage], str]:
    # process time_range, start_date, end_date
    time_range = "one_month" if demo else time_range
    start_date, end_date, time_str = use_time_range(time_range, start_date, end_date)

    # fetch data, either using demo or user method
    if demo:
        output = await get_user_demo(user_id, start_date, end_date, no_cache=no_cache)
    else:
        output = await get_user(user_id, start_date, end_date, no_cache=no_cache)

    return output, time_str
