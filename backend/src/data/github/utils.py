from typing import Optional

from src.data.mongo.secret import get_random_key


def get_access_token(access_token: Optional[str] = None) -> str:
    return access_token if access_token is not None else get_random_key()
