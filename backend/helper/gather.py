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


async def gather_with_concurrency(
    n: int, *tasks: List[Callable[..., Any]]
) -> List[Any]:
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task: Callable[..., Any]) -> Any:
        async with semaphore:
            return await task  # type: ignore

    return await asyncio.gather(*(sem_task(task) for task in tasks))  # type: ignore


async def _gather(
    funcs: List[Callable[..., Any]],
    args_dicts: List[Dict[str, Any]],
    max_threads: int = 5,
) -> List[Any]:
    """runs the given functions asynchronously"""

    async_funcs = [async_function(func) for func in funcs]

    output: List[Any] = list(
        await gather_with_concurrency(
            max_threads,
            *(
                async_func(**kwargs)
                for async_func, kwargs in zip(async_funcs, args_dicts)
            )
        )
    )

    return output


def gather(
    funcs: List[Callable[..., Any]],
    args_dicts: List[Dict[str, Any]],
    max_threads: int = 5,
) -> List[Any]:
    """runs the given functions asynchronously"""

    return asyncio.run(
        _gather(funcs=funcs, args_dicts=args_dicts, max_threads=max_threads)
    )
