import logging
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.constants import OAUTH_CLIENT_ID
from src.processing.auth import authenticate, delete_user
from src.routers.decorators import get_redirect_url

router = APIRouter()


@router.get("/signup/public")
def redirect_public(user_id: Optional[str] = None) -> RedirectResponse:
    return RedirectResponse(get_redirect_url(private=False, user_id=user_id))


@router.get("/signup/private")
def redirect_private(user_id: Optional[str] = None) -> RedirectResponse:
    return RedirectResponse(get_redirect_url(private=True, user_id=user_id))


@router.get("/redirect", include_in_schema=False)
async def redirect_return(code: str = "", private_access: bool = False) -> str:
    try:
        user_id = await authenticate(code=code, private_access=private_access)
        return f"You ({user_id}) are now authenticated!"
    except Exception as e:
        logging.exception(e)
        return "Unknown Error. Please try again later."


@router.get("/delete/{user_id}")
async def delete_account_auth(user_id: str) -> RedirectResponse:
    return RedirectResponse(
        get_redirect_url(prefix=f"delete/{user_id}", private=False, user_id=user_id)
    )


@router.get("/redirect/delete/{user_id}", include_in_schema=False)
async def delete_account(user_id: str) -> RedirectResponse:
    await delete_user(user_id, user_key="", use_user_key=False)
    return RedirectResponse(
        f"https://github.com/settings/connections/applications/{OAUTH_CLIENT_ID}"
    )
