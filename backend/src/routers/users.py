from datetime import date, datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, Response, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

import svgwrite  # type: ignore

from src.db.models.users import UserModel as DBUserModel
from src.db.functions.users import login_user
from src.db.functions.get import get_user_by_user_id

from src.constants import PUBSUB_PUB
from src.external.pubsub.templates import publish_to_topic
from src.utils import async_fail_gracefully, svg_fail_gracefully

router = APIRouter()


@router.get("/db/create/{user_id}/{access_token}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def create_user_endpoint(
    response: Response, user_id: str, access_token: str
) -> str:
    return await login_user(user_id, access_token)


@router.get("/db/get/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user_endpoint(response: Response, user_id: str) -> Optional[DBUserModel]:
    return await get_user_by_user_id(user_id)


async def _get_user(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Dict[str, Any]:
    if not PUBSUB_PUB:
        raise HTTPException(400, "")

    db_user = await get_user_by_user_id(user_id)
    if db_user is None or db_user.access_token == "":
        raise LookupError("Invalid UserId")

    if db_user.raw_data is not None and (
        datetime.now() - db_user.last_updated
    ) < timedelta(hours=6):
        return db_user.raw_data

    publish_to_topic(
        "user",
        {
            "user_id": user_id,
            "access_token": db_user.access_token,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "timezone_str": timezone_str,
        },
    )

    return {}


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def get_user(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Dict[str, Any]:
    return await _get_user(user_id, start_date, end_date, timezone_str)


@router.get(
    "/{user_id}/svg", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
@svg_fail_gracefully
async def get_user_svg(
    response: Response,
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Any:
    # output = await _get_user(user_id, start_date, end_date, timezone_str)
    old = """
    <svg width="300" height="285">
        <rect
          x="0.5"
          y="0.5"
          rx="4.5"
          height="99%"
          stroke="#e4e2e2"
          width="299"
          fill="#fffefe"
          stroke-opacity="1"
        />
        <g transform="translate(25, 35)">
            <text x="0" y="0" class="header">Most Used Languages</text>
        </g>
        <g transform="translate(0, 55)">
            <svg x="25">
                <g transform="translate(0, 0)">
                    <text x="2" y="15" class="lang-name">Jupyter Notebook</text>
                    <text x="215" y="34" class="lang-name">73.16%</text>
                    <svg width="205" x="0" y="25">
                        <rect rx="5" ry="5" x="0" y="0" width="205" height="8" fill="#ddd" />
                        <rect height="8" fill="#DA5B0B" rx="5" ry="5" x="0" width="73.16%" />
                    </svg>
                </g>
            </svg>
        </g>
    </svg>
    """

    print(old)

    style = """
        .header {
            font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
            fill: #2f80ed;
            animation: fadeInAnimation 0.8s ease-in-out forwards;
        }
        .lang-name {
            font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif;
            fill: #333;
        }

        @keyframes fadeInAnimation {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
    """

    d = svgwrite.Drawing(size=(300, 285))
    d.defs.add(d.style(style))  # type: ignore
    d.add(  # type: ignore
        d.rect(  # type: ignore
            size=(299, 284),
            insert=(0.5, 0.5),
            rx=4.5,
            stroke="#e4e2e2",
            fill="#fffefe",
        )
    )
    d.add(d.text("Most Used Languages", insert=(25, 35), class_="header"))  # type: ignore

    return d
