from src.data.mongo.main import USER_MONTHS
from src.data.mongo.user_months.models import UserMonth


async def set_user_month(user_month: UserMonth):
    compressed_user_month = user_month.model_dump()
    compressed_user_month["data"] = user_month.data.compress()

    await USER_MONTHS.update_one(
        {"user_id": user_month.user_id, "month": user_month.month},
        {"$set": compressed_user_month},
        upsert=True,
    )
