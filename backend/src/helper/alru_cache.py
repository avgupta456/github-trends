from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple


# NOTE: return flag = False to avoid caching
# considers two optional parameters
# if ignore_cache=True provided, bypass cache system and do not save to cache
# if ignore_cache=True and update_cache=True, bypass cache and save result to cache
# otherwise, use cache normally
def alru_cache(max_size: int = 128, ttl: timedelta = timedelta(minutes=5)):
    def decorator(func: Callable[..., Any]) -> Any:
        cache: Dict[Any, Tuple[datetime, Any]] = {}
        keys: List[Any] = []

        def in_cache(key: Any) -> bool:
            # key not in cache
            if key not in cache:
                return False

            # key in cache but expired
            if datetime.now() - cache[key][0] > ttl:
                return False

            # key in cache and not expired
            return True

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
                {
                    k: v
                    for k, v in kwargs.items()
                    if k not in ["ignore_cache", "update_cache"]
                }
            )
            if "ignore_cache" in kwargs and kwargs["ignore_cache"]:
                (flag, value) = await func(*args, **kwargs)
                if "update_cache" in kwargs and kwargs["update_cache"]:
                    return update_cache_and_return(key, flag, value)
                return value

            if in_cache(key):
                return cache[key][1]

            (flag, value) = await func(*args, **kwargs)
            return update_cache_and_return(key, flag, value)

        return wrapper

    return decorator
