import logging
import io

from datetime import datetime, date, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple

from fastapi import Response, status

from svgwrite.drawing import Drawing  # type: ignore

from src.svg.error import get_error_svg


def fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    def wrapper(response: Response, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        start = datetime.now()
        try:
            data = func(response, *args, **kwargs)
            return {"data": data, "message": "200 OK", "time": datetime.now() - start}
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "data": [],
                "message": "Error " + str(e),
                "time": datetime.now() - start,
            }

    return wrapper


def async_fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        start = datetime.now()
        try:
            data = await func(response, *args, **kwargs)
            return {"data": data, "message": "200 OK", "time": datetime.now() - start}
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "data": [],
                "message": "Error " + str(e),
                "time": datetime.now() - start,
            }

    return wrapper


# NOTE: returns HTTP_200_OK regardless to avoid retrying PubSub API
def pubsub_fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        start = datetime.now()
        try:
            data = await func(response, *args, **kwargs)
            return {"data": data, "message": "200 OK", "time": datetime.now() - start}
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_200_OK
            return {
                "data": [],
                "message": "Error " + str(e),
                "time": datetime.now() - start,
            }

    return wrapper


# NOTE: implied async, sync not implemented yet
def svg_fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        d: Drawing
        status_code: int
        start = datetime.now()
        try:
            d = await func(response, *args, **kwargs)
            status_code = status.HTTP_200_OK
        except Exception as e:
            logging.exception(e)
            d = get_error_svg()
            status_code = status.HTTP_200_OK

        sio = io.StringIO()
        d.write(sio)  # type: ignore

        print(datetime.now() - start)

        return Response(
            sio.getvalue(), media_type="image/svg+xml", status_code=status_code
        )

    return wrapper


def date_to_datetime(
    dt: date, hour: int = 0, minute: int = 0, second: int = 0
) -> datetime:

    return datetime(dt.year, dt.month, dt.day, hour, minute, second)


# returns start date, end date, string representing time range
def use_time_range(
    time_range: str, start_date: date, end_date: date
) -> Tuple[date, date, str]:
    duration_options = {
        "one_month": (30, "Past 1 Month"),
        "six_months": (180, "Past 6 Months"),
        "one_year": (365, "Past 1 Year"),
        "five_years": (365 * 5, "Past 5 Years"),
    }

    start_str = start_date.strftime("X%m/X%d/%Y").replace("X0", "X").replace("X", "")
    end_str = end_date.strftime("X%m/X%d/%Y").replace("X0", "X").replace("X", "")
    if end_date == date.today():
        end_str = "Present"
    time_str = start_str + " - " + end_str

    if time_range in duration_options:
        days, time_str = duration_options[time_range]
        end_date = date.today()
        start_date = date.today() - timedelta(days)

    return start_date, end_date, time_str
