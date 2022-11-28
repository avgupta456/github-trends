from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple


# NOTE: return flag = False to avoid caching
# considers one optional parameter, no_cache
# if true, bypass cache system, otherwise use normally
def alru_cache(max_size: int = 128, ttl: timedelta = timedelta(minutes=1)):
    def decorator(func: Callable[..., Any]) -> Any:
        cache: Dict[Any, Tuple[datetime, Any]] = {}
        keys: List[Any] = []

        def in_cache(key: Any) -> bool:
            # key not in cache
            return False if key not in cache else datetime.now() - cache[key][0] <= ttl

        def update_cache_and_return(key: Any, flag: bool, value: Any) -> Any:
            # if flag = False, do not update cache and return value
            if not flag:
                return value

            # if flag = True, update cache
            now = datetime.now()
            cache[key] = (now, value)
            keys.append(key)

            # remove oldest key if cache is full
            if len(keys) > max_size:
                del cache[keys.pop(0)]

            # return value from cache
            return cache[key][1]

        @wraps(func)
        async def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            key = tuple(args), frozenset(
                {k: v for k, v in kwargs.items() if k not in ["no_cache"]}
            )
            if "no_cache" in kwargs and kwargs["no_cache"]:
                (flag, value) = await func(*args, **kwargs)
                return update_cache_and_return(key, flag, value)

            if in_cache(key):
                return cache[key][1]

            (flag, value) = await func(*args, **kwargs)
            return update_cache_and_return(key, flag, value)

        return wrapper

    return decorator
