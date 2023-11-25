from datetime import date
from typing import Optional, Tuple

from src.aggregation.layer2.user import get_user, get_user_demo
from src.models import UserPackage
from src.models.background import UpdateUserBackgroundTask
from src.utils import use_time_range


async def svg_base(
    user_id: str,
    start_date: date,
    end_date: date,
    time_range: str,
    demo: bool,
    no_cache: bool = False,
) -> Tuple[Optional[UserPackage], bool, Optional[UpdateUserBackgroundTask], str]:
    # process time_range, start_date, end_date
    time_range = "one_month" if demo else time_range
    start_date, end_date, time_str = use_time_range(time_range, start_date, end_date)
    complete = True  # overwritten later if not complete
    background_task = None

    # fetch data, either using demo or user method
    if demo:
        output = await get_user_demo(user_id, start_date, end_date, no_cache=no_cache)
    else:
        output, complete, background_task = await get_user(
            user_id, start_date, end_date, no_cache=no_cache
        )

    return output, complete, background_task, time_str
