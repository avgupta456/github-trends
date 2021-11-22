from src.constants import WRAPPED_VERSION
from src.data.mongo.main import WRAPPED
from src.models import WrappedPackage


async def set_wrapped_user(
    user_id: str, year: int, private: bool, data: WrappedPackage
) -> None:
    await WRAPPED.update_one(  # type: ignore
        {"user_id": user_id, "year": year, "private": private},
        {"$set": {"data": data.dict(), "version": WRAPPED_VERSION}},
        upsert=True,
    )
