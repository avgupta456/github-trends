from datetime import datetime, timedelta
from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    FrozenSet,
    List,
    ParamSpec,
    Tuple,
    TypeVar,
)

Param = ParamSpec("Param")
TOutput = TypeVar("TOutput")

TKey = Tuple[Tuple[Any, ...], FrozenSet[Tuple[str, Any]]]


def alru_cache(max_size: int = 128, ttl: timedelta = timedelta(minutes=1)):
    def decorator(
        func: Callable[Param, Awaitable[Tuple[bool, TOutput]]]
    ) -> Callable[Param, Awaitable[TOutput]]:
        cache: Dict[TKey, Tuple[datetime, TOutput]] = {}
        keys: List[TKey] = []

        def in_cache(key: TKey) -> bool:
            # key not in cache
            if key not in cache:
                return False

            # key in cache but expired
            if datetime.now() - cache[key][0] > ttl:
                return False

            # key in cache and not expired
            return True

        def update_cache_and_return(key: TKey, flag: bool, value: TOutput) -> TOutput:
            # if flag = False, do not update cache and return value
            if not flag:
                return value

            # if flag = True, update cache
            now = datetime.now()
            cache[key] = (now, value)
            keys.append(key)

            # remove oldest key if cache is full
            if len(keys) > max_size:
                try:
                    # Should not raise KeyError, but just in case
                    del cache[keys.pop(0)]
                except KeyError:
                    # Already deleted by another thread
                    pass

            # return value from cache
            return value  # equal to cache[key][1]

        @wraps(func)
        async def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> TOutput:
            key: TKey = tuple(args), frozenset(
                [(k, v) for k, v in kwargs.items() if k not in ["no_cache"]]
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
