from datetime import date, timedelta
from functools import lru_cache
from typing import Any, Dict

from packaging.user import main as get_data

from analytics.user.commits import get_top_languages, get_top_repos
from analytics.user.contribs_per_day import (
    get_contribs_per_day,
    get_contribs_per_repo_per_day,
)


from helper.gather import gather


@lru_cache(maxsize=1024)
def main(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> Dict[str, Any]:
    data = get_data(user_id, start_date, end_date, timezone_str)

    funcs = [
        get_top_languages,
        get_top_repos,
        get_contribs_per_day,
        get_contribs_per_repo_per_day,
    ]
    [top_languages, top_repos, contribs_per_day, contribs_per_repo_per_day] = gather(
        funcs=funcs, args_dicts=[{"data": data} for _ in range(len(funcs))]
    )

    return {
        "top_languages": top_languages,
        "top_repos": top_repos,
        "contribs_per_day": contribs_per_day,
        "contribs_per_repo_per_day": contribs_per_repo_per_day,
    }
