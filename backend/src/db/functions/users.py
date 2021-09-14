from src.db.mongodb import USERS


async def create_user(user_id: str, access_token: str) -> str:
    await USERS.update_one(  # type: ignore
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "access_token": access_token}},
        upsert=True,
    )
    return user_id
