from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient

from src.constants import LOCAL, MONGODB_PASSWORD, PROD


def get_conn_str(password: str, database: str) -> str:
    return f"mongodb+srv://root:{password}@backend2.e50j8dp.mongodb.net/{database}?retryWrites=true&w=majority"


if LOCAL:
    DB = None
elif PROD:
    conn_str = get_conn_str(MONGODB_PASSWORD, "prod_backend")
    CLIENT = AsyncIOMotorClient(
        conn_str, serverSelectionTimeoutMS=5000, tlsInsecure=True
    )
    DB = CLIENT.prod_backend  # type: ignore
else:
    conn_str = get_conn_str(MONGODB_PASSWORD, "dev_backend")
    CLIENT = AsyncIOMotorClient(  # type: ignore
        conn_str, serverSelectionTimeoutMS=5000, tlsInsecure=True
    )
    DB = CLIENT.dev_backend  # type: ignore

# Overwrite type since only None if Local=True
SECRETS: AgnosticCollection = None if DB is None else DB.secrets  # type: ignore
USERS: AgnosticCollection = None if DB is None else DB.users  # type: ignore
USER_MONTHS: AgnosticCollection = None if DB is None else DB.user_months  # type: ignore
