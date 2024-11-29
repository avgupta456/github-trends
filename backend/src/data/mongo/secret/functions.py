from datetime import timedelta
from random import randint
from typing import Any, Dict, List, Optional, Tuple

from src.constants import TEST_TOKEN
from src.data.mongo.main import SECRETS
from src.data.mongo.secret.models import SecretModel
from src.utils import alru_cache


@alru_cache(ttl=timedelta(minutes=15))
async def get_keys(no_cache: bool = False) -> Tuple[bool, List[str]]:
    secrets: Optional[Dict[str, Any]] = await SECRETS.find_one({"project": "main"})
    if secrets is None:
        return (False, [])

    tokens = SecretModel.model_validate(secrets).access_tokens
    return (True, tokens)


secret_keys: List[str] = []


async def update_keys(no_cache: bool = False) -> None:
    global secret_keys
    secret_keys = await get_keys(no_cache=no_cache)


def get_random_key() -> str:
    global secret_keys
    if len(secret_keys) == 0:
        return TEST_TOKEN

    return secret_keys[randint(0, len(secret_keys) - 1)]
