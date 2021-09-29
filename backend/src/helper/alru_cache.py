from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple


# NOTE: return None to avoid caching
def alru_cache(max_size: int = 128, ttl: timedelta = timedelta(hours=1)):
    def decorator(func: Callable[..., Any]) -> Any:
        cache: Dict[Any, Tuple[datetime, Any]] = {}
        keys: List[Any] = []

        @wraps(func)
        async def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            now = datetime.now()
            key = tuple(args), frozenset(kwargs.items())
            if key not in cache or now - cache[key][0] > ttl:
                (flag, value) = await func(*args, **kwargs)
                if not flag:
                    return value
                cache[key] = (now, value)
                keys.append(key)
                if len(keys) > max_size:
                    del cache[keys.pop(0)]
            return cache[key][1]

        return wrapper

    return decorator
