# type: ignore

from motor.motor_asyncio import AsyncIOMotorClient

from src.constants import MONGODB_PASSWORD, PROD


def get_conn_str(password: str, database: str) -> str:
    return f"mongodb://root:{password}@backend-shard-00-00.aqlpb.mongodb.net:27017,backend-shard-00-01.aqlpb.mongodb.net:27017,backend-shard-00-02.aqlpb.mongodb.net:27017/{database}?ssl=true&replicaSet=atlas-25pkcv-shard-0&authSource=admin&retryWrites=true&w=majority"


if PROD:
    conn_str = get_conn_str(MONGODB_PASSWORD, "prod_backend")
    CLIENT = AsyncIOMotorClient(
        conn_str, serverSelectionTimeoutMS=5000, tlsInsecure=True
    )
    DB = CLIENT.prod_backend
else:
    conn_str = get_conn_str(MONGODB_PASSWORD, "dev_backend")
    CLIENT = AsyncIOMotorClient(
        conn_str, serverSelectionTimeoutMS=5000, tlsInsecure=True
    )
    DB = CLIENT.dev_backend

USERS = DB.users
SECRETS = DB.secrets
WRAPPED = DB.wrapped
