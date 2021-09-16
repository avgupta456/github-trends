import logging
import io

from datetime import datetime, date
from functools import wraps
from typing import Any, Callable, Dict, List

from fastapi import Response, status

from svgwrite.drawing import Drawing  # type: ignore


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


# NOTE: implied async, sync not implemented yet
def svg_fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        d: Drawing
        status_code: int
        try:
            d = await func(response, *args, **kwargs)
            status_code = status.HTTP_200_OK
        except Exception as e:
            logging.exception(e)
            d = Drawing()
            d.add(d.text("Unknown Error"))  # type: ignore
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        sio = io.StringIO()
        d.write(sio)  # type: ignore

        return Response(
            sio.getvalue(), media_type="image/svg+xml", status_code=status_code
        )

    return wrapper


def date_to_datetime(
    dt: date, hour: int = 0, minute: int = 0, second: int = 0
) -> datetime:

    return datetime(dt.year, dt.month, dt.day, hour, minute, second)
