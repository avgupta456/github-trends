from datetime import timedelta
from random import randint
from typing import Any, Dict, List, Optional

from src.constants import TEST_TOKEN
from src.data.mongo.main import SECRETS  # type: ignore
from src.data.mongo.secret.models import SecretModel
from src.utils import alru_cache


@alru_cache(ttl=timedelta(minutes=15))
async def get_keys(no_cache: bool = False) -> List[str]:
    secrets: Optional[Dict[str, Any]] = await SECRETS.find_one({"project": "main"})  # type: ignore
    if secrets is None:
        return (False, [])  # type: ignore

    tokens = SecretModel.parse_obj(secrets).access_tokens
    return (True, tokens)  # type: ignore


secret_keys: List[str] = []


async def update_keys() -> None:
    global secret_keys
    secret_keys = await get_keys()


def get_random_key() -> str:
    global secret_keys
    if len(secret_keys) == 0:
        return TEST_TOKEN

    return secret_keys[randint(0, len(secret_keys) - 1)]
