from datetime import timedelta
from random import randint
from typing import Any, Dict, List, Optional

from src.data.mongo.main import SECRETS
from src.data.mongo.secret.models import SecretModel
from src.utils import alru_cache


@alru_cache(ttl=timedelta(minutes=15))
async def get_keys(project: str, no_cache: bool = False) -> List[str]:
    secrets: Optional[Dict[str, Any]] = await SECRETS.find_one({"project": project})  # type: ignore
    if secrets is None:
        return (False, [])  # type: ignore

    tokens = SecretModel.parse_obj(secrets).access_tokens
    return (True, tokens)  # type: ignore


async def get_next_key(project: str, no_cache: bool = False) -> str:
    keys: List[str] = await get_keys(project, no_cache=no_cache)
    if len(keys) == 0:
        return ""

    return keys[randint(0, len(keys) - 1)]
