import asyncio
from functools import partial, wraps
from typing import Any, Callable, Dict, List


def async_function(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def run(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor=None, func=pfunc)

    return run


async def _gather(
    funcs: List[Callable[..., Any]], args_dicts: List[Dict[str, Any]]
) -> List[Any]:
    """runs the given functions asynchronously"""

    async_funcs = [async_function(func) for func in funcs]

    output: List[Any] = list(
        await asyncio.gather(
            *(
                async_func(**kwargs)
                for async_func, kwargs in zip(async_funcs, args_dicts)
            )
        )
    )

    return output


def gather(
    funcs: List[Callable[..., Any]], args_dicts: List[Dict[str, Any]]
) -> List[Any]:
    """runs the given functions asynchronously"""

    return asyncio.run(_gather(funcs=funcs, args_dicts=args_dicts))
