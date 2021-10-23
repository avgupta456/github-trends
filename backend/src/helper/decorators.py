import logging
import io

from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, List

from fastapi import Response, status
from starlette.responses import RedirectResponse

from svgwrite.drawing import Drawing  # type: ignore

from src.svg.error import get_error_svg
from src.helper.utils import get_redirect_url


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
        start = datetime.now()
        try:
            d = await func(response, *args, **kwargs)
        except LookupError as e:
            if "user_id" in kwargs:
                user_id: str = kwargs["user_id"]  # type: ignore
                url = get_redirect_url(private=False, user_id=user_id)
                return RedirectResponse(url)
            logging.exception(e)
            d = get_error_svg()
        except Exception as e:
            logging.exception(e)
            d = get_error_svg()

        sio = io.StringIO()
        d.write(sio)  # type: ignore

        print(datetime.now() - start)

        return Response(
            sio.getvalue(), media_type="image/svg+xml", status_code=status.HTTP_200_OK
        )

    return wrapper
