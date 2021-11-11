from datetime import datetime

from src.data.mongo.main import WRAPPED
from src.models import WrappedPackage


async def lock_wrapped_user(user_id: str, year: int) -> None:
    await WRAPPED.update_one(  # type: ignore
        {"user_id": user_id, "year": year}, {"$set": {"lock": datetime.now()}}
    )


async def set_wrapped_user(user_id: str, year: int, data: WrappedPackage) -> None:
    await WRAPPED.update_one(  # type: ignore
        {"user_id": user_id, "year": year},
        {"$set": {"data": data.dict(), "version": 1}},
        upsert=True,
    )
