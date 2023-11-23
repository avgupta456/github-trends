import io
import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from fastapi import Response, status
from starlette.responses import RedirectResponse
from svgwrite.drawing import Drawing  # type: ignore

from src.constants import OAUTH_CLIENT_ID, OAUTH_REDIRECT_URI
from src.render import get_error_svg


# for standalone auth routes
def get_redirect_url(
    prefix: str = "", private: bool = False, user_id: Optional[str] = None
) -> str:
    url = (
        "https://github.com/login/oauth/authorize?client_id="
        + OAUTH_CLIENT_ID
        + "&redirect_uri="
        + OAUTH_REDIRECT_URI
        + "/redirect"
    )

    # add prefix to redirect to different backend routes
    if prefix != "":
        url += f"/{prefix}"

    # add private flag to request correct permissions
    if private:
        url += "?private_access=True&scope=user,repo"
    else:
        url += "?private_access=False"

    # add user_id to hint if provided
    if user_id is not None:
        url += f"&login={user_id}"

    return url


# NOTE: implied async, sync not implemented yet
def svg_fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        d: Drawing
        start = datetime.now()
        cache_max_age = 3600
        try:
            d = await func(response, *args, **kwargs)
        except LookupError as e:
            if "user_id" in kwargs:
                user_id: str = kwargs["user_id"]  # type: ignore
                url = get_redirect_url(private=False, user_id=user_id)
                return RedirectResponse(url)
            logging.exception(e)
            d = get_error_svg()
            cache_max_age = 0
        except Exception as e:
            logging.exception(e)
            d = get_error_svg()
            cache_max_age = 0

        sio = io.StringIO()
        d.write(sio)  # type: ignore

        print("SVG", datetime.now() - start)

        return Response(
            sio.getvalue(),
            media_type="image/svg+xml",
            status_code=status.HTTP_200_OK,
            headers={"Cache-Control": f"public, max-age={cache_max_age}"},
        )

    return wrapper
