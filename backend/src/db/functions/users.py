from src.db.models.users import UserModel

from src.db.mongodb import USERS


async def create_user(user_id: str, access_token: str) -> str:
    user = UserModel.parse_obj({"user_id": user_id, "access_token": access_token})
    await USERS.insert_one(user.dict())  # type: ignore
    return user_id
