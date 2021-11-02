from typing import Any, Optional

import logging

from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse

from src.publisher.processing import authenticate, delete_user
from src.publisher.routers.decorators import get_redirect_url

from src.constants import BACKEND_URL
from src.utils import async_fail_gracefully

router = APIRouter()


@router.post("/login/{code}", status_code=status.HTTP_200_OK)
@async_fail_gracefully
async def authenticate_endpoint(
    response: Response, code: str, private_access: bool = False
) -> str:
    return await authenticate(code, private_access)


# TODO: reset cache upon upgrade, downgrade, or delete


@router.get("/signup/public")
def redirect_public(user_id: Optional[str] = None) -> RedirectResponse:
    return RedirectResponse(get_redirect_url(private=False, user_id=user_id))


@router.get("/signup/private")
def redirect_private(user_id: Optional[str] = None) -> RedirectResponse:
    return RedirectResponse(get_redirect_url(private=True, user_id=user_id))


@router.get("/redirect")
async def redirect_return(
    code: str = "", private_access: bool = False
) -> RedirectResponse:
    try:
        user_id = await authenticate(code=code, private_access=private_access)  # type: ignore
        return RedirectResponse(BACKEND_URL + "/auth/redirect_success/" + user_id)
    except Exception as e:
        logging.exception(e)
        return RedirectResponse(BACKEND_URL + "/auth/redirect_failure")


@router.get("/redirect_success/{user_id}")
def redirect_success(user_id: str) -> str:
    return "You (" + user_id + ") are now authenticated!"


@router.get("/redirect_failure")
def redirect_failure() -> str:
    return "Unknown Error. Please try again later."


@router.get("/delete/{user_id}")
async def delete_account_auth(user_id: str, redirect: bool = True) -> Any:
    if redirect:
        return RedirectResponse(
            get_redirect_url(prefix="delete/" + user_id, private=False, user_id=user_id)
        )

    # TODO: setup CORS by route to allow adding "await delete_user(user_id)" without security concerns

    return await delete_user(user_id)


@router.get("/redirect/delete/{user_id}")
async def delete_account(user_id: str) -> RedirectResponse:
    redirect = await delete_user(user_id)
    return RedirectResponse(redirect)
