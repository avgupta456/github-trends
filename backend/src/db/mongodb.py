# type: ignore

from motor.motor_asyncio import AsyncIOMotorClient

from src.constants import PROD, MONGODB_PASSWORD

if PROD:
    conn_str = f"mongodb+srv://root:{MONGODB_PASSWORD}@backend.aqlpb.mongodb.net/prod_backend?retryWrites=true&w=majority"
    CLIENT = AsyncIOMotorClient(
        conn_str, serverSelectionTimeoutMS=5000, tlsInsecure=True
    )
    DB = CLIENT.prod_backend
else:
    conn_str = f"mongodb+srv://root:{MONGODB_PASSWORD}@backend.aqlpb.mongodb.net/dev_backend?retryWrites=true&w=majority"
    CLIENT = AsyncIOMotorClient(
        conn_str, serverSelectionTimeoutMS=5000, tlsInsecure=True
    )
    DB = CLIENT.dev_backend

USERS = DB.users
SECRETS = DB.secrets
