from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from src.constants import PROD, MONGODB_PASSWORD

if PROD:
    conn_str = f"mongodb+srv://root:{MONGODB_PASSWORD}@backend.aqlpb.mongodb.net/prod_backend?retryWrites=true&w=majority"
    CLIENT = AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)  # type: ignore
    DB = CLIENT.prod_backend  # type: ignore
else:
    conn_str = f"mongodb+srv://root:{MONGODB_PASSWORD}@backend.aqlpb.mongodb.net/dev_backend?retryWrites=true&w=majority"
    CLIENT = AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)  # type: ignore
    DB = CLIENT.dev_backend  # type: ignore

USERS = DB.users  # type: ignore
