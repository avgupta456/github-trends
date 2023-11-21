from src.publisher.routers.assets.assets import router as asset_router
from src.publisher.routers.auth.main import router as auth_router
from src.publisher.routers.users.main import router as user_router

__all__ = ["asset_router", "user_router", "auth_router"]
