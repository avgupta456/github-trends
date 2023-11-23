from fastapi import APIRouter

from src.routers.auth.standalone import router as standalone_router
from src.routers.auth.website import router as website_router

router = APIRouter()
router.include_router(standalone_router, prefix="")
router.include_router(website_router, prefix="/web")
