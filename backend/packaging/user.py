import asyncio
from asyncio.events import AbstractEventLoop
from functools import wraps, partial
from typing import Any, Callable, Dict, List, Optional, Union

from processing.user.contribution_calendar import get_user_contribution_calendar
from processing.user.contribution_commits import get_user_contribution_commits
from processing.user.contribution_stats import get_user_contribution_stats
from processing.user.follows import get_user_followers

from models.user.contribution_calendar import UserContribCalendar as ContribCalendar
from models.user.contribution_commits import UserContribCommits as ContribCommits
from models.user.contribution_stats import UserContribStats as ContribStats
from models.user.follows import UserFollows as Follows
from models.misc.date import Date, today
from models.user.user import UserPackage


def async_function(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def run(
        *args: List[Any],
        loop: Optional[AbstractEventLoop] = None,
        executor: Any = None,
        **kwargs: Dict[str, Any],
    ) -> Any:
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


async def _main(
    user_id: str,
    max_repos: int = 100,
    start_date: Date = today - 365,
    end_date: Date = today,
) -> UserPackage:
    output: List[Union[ContribCalendar, ContribCommits, ContribStats, Follows]] = list(
        await asyncio.gather(
            async_function(get_user_contribution_calendar)(user_id=user_id, start_date=start_date, end_date=end_date),  # type: ignore
            async_function(get_user_contribution_commits)(user_id=user_id, max_repos=max_repos, start_date=start_date, end_date=end_date),  # type: ignore
            async_function(get_user_contribution_stats)(user_id=user_id, max_repos=max_repos, start_date=start_date, end_date=end_date),  # type: ignore
            async_function(get_user_followers)(user_id=user_id),  # type: ignore
        )
    )

    types = Union[ContribCalendar, ContribCommits, ContribStats, Follows, None]
    array: List[types] = [None for _ in range(4)]
    types = [ContribCalendar, ContribCommits, ContribStats, Follows]
    for i, type in enumerate(types):
        array[i] = list(filter(lambda x: isinstance(x, type), output))[0]

    user_package = UserPackage(
        contribution_calendar=array[0],
        contribution_commits=array[1],
        contribution_stats=array[2],
        follows=array[3],
    )

    return user_package


def main(
    user_id: str,
    max_repos: int = 100,
    start_date: Date = today - 365,
    end_date: Date = today,
) -> UserPackage:
    return asyncio.run(
        _main(
            user_id=user_id,
            max_repos=max_repos,
            start_date=start_date,
            end_date=end_date,
        )
    )
