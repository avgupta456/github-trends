from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any, DefaultDict, Dict, List, Optional, Set, Union

import pytz

from src.constants import NODE_CHUNK_SIZE, NODE_THREADS
from src.data.github.graphql import (
    RawCalendar,
    RawEventsCommit,
    RawEventsEvent,
    RawRepo,
    get_repo,
    get_user_contribution_calendar,
    get_user_contribution_events,
    get_user_contribution_years,
)
from src.data.github.rest import RawCommit
from src.models import UserContributions
from src.models.user.contribs import FullUserContributions
from src.subscriber.aggregation.user.commit import (
    get_all_commit_info,
    get_commits_languages,
)
from src.utils import date_to_datetime, gather

t_stats = DefaultDict[str, Dict[str, List[Union[RawEventsEvent, RawEventsCommit]]]]
t_commits = List[Dict[str, Union[Dict[str, Dict[str, Union[str, int]]], str]]]
t_languages = List[Dict[str, Dict[str, Union[str, int]]]]


def get_user_all_contribution_events(
    user_id: str,
    start_date: datetime,
    end_date: datetime,
    access_token: Optional[str] = None,
) -> t_stats:
    repo_contribs: t_stats = defaultdict(
        lambda: {"commits": [], "issues": [], "prs": [], "reviews": [], "repos": []}
    )
    after: Optional[str] = ""
    index, cont = 0, True
    while index < 10 and cont:
        after_str = after if isinstance(after, str) else ""
        response = get_user_contribution_events(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            after=after_str,
            access_token=access_token,
        )

        cont = False
        for event_type, event_list in zip(
            ["commits", "issues", "prs", "reviews"],
            [
                response.commit_contribs_by_repo,
                response.issue_contribs_by_repo,
                response.pr_contribs_by_repo,
                response.review_contribs_by_repo,
            ],
        ):
            for repo in event_list:
                name = repo.repo.name
                for event in repo.contribs.nodes:
                    repo_contribs[name][event_type].append(event)
                if repo.contribs.page_info.has_next_page:
                    after = repo.contribs.page_info.end_cursor
                    cont = True

        for repo in response.repo_contribs.nodes:
            name = repo.repo.name
            repo_contribs[name]["repos"].append(
                RawEventsEvent(occurredAt=str(repo.occurred_at))
            )

        index += 1

    return repo_contribs


async def get_contributions(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
    full: bool = False,
    access_token: Optional[str] = None,
) -> Union[UserContributions, FullUserContributions]:
    tz = pytz.timezone(timezone_str)

    # get years for contribution calendar
    years = sorted(
        filter(
            lambda x: start_date.year <= x <= end_date.year,
            get_user_contribution_years(user_id, access_token),
        )
    )

    dates = [
        [
            date_to_datetime(max(date(year, 1, 1), start_date)),
            date_to_datetime(
                min(date(year, 12, 31), end_date), hour=23, minute=59, second=59
            ),
        ]
        for year in years
    ]

    # async get contribution calendars
    calendars: List[RawCalendar] = await gather(
        funcs=[get_user_contribution_calendar for _ in years],
        args_dicts=[
            {
                "user_id": user_id,
                "start_date": dates[i][0],
                "end_date": dates[i][1],
                "access_token": access_token,
            }
            for i in range(len(years))
        ],
    )

    all_events: List[t_stats] = await gather(
        funcs=[get_user_all_contribution_events for _ in years],
        args_dicts=[
            {
                "user_id": user_id,
                "start_date": dates[i][0],
                "end_date": dates[i][1],
                "access_token": access_token,
            }
            for i in range(len(years))
        ],
    )

    repos_set: Set[str] = set()
    for events_year in all_events:
        for repo in events_year:
            repos_set.add(repo)
    repos = list(repos_set)

    commit_infos: List[List[RawCommit]] = await gather(
        funcs=[get_all_commit_info for _ in repos],
        args_dicts=[
            {
                "user_id": user_id,
                "name_with_owner": repo,
                "start_date": dates[0][0],  # first start
                "end_date": dates[-1][1],  # last end
                "access_token": access_token,
            }
            for repo in repos
        ],
        max_threads=100,
    )

    _repo_infos: List[Optional[RawRepo]] = await gather(
        funcs=[get_repo for _ in repos],
        args_dicts=[
            {
                "owner": repo.split("/")[0],
                "repo": repo.split("/")[1],
                "access_token": access_token,
            }
            for repo in repos
        ],
        max_threads=100,
    )

    repo_infos = {
        repo: repo_info
        for repo, repo_info in zip(repos, _repo_infos)
        if repo_info is not None
    }

    commit_times = [[x.timestamp for x in repo] for repo in commit_infos]
    commit_node_ids = [[x.node_id for x in repo] for repo in commit_infos]

    id_mapping: Dict[str, List[int]] = {}
    repo_mapping: Dict[str, str] = {}
    all_node_ids: List[str] = []
    for i, repo_node_ids in enumerate(commit_node_ids):
        for j, node_id in enumerate(repo_node_ids):
            id_mapping[node_id] = [i, j]
            repo_mapping[node_id] = repos[i]
            all_node_ids.append(node_id)

    node_id_chunks: List[List[str]] = []
    commit_repo_chunks: List[List[str]] = []
    for i in range(0, len(all_node_ids), NODE_CHUNK_SIZE):
        node_id_chunks.append(
            all_node_ids[i : min(len(all_node_ids), i + NODE_CHUNK_SIZE)]
        )
        commit_repo_chunks.append(
            [repo_mapping[node_id] for node_id in node_id_chunks[-1]]
        )

    max_threads = NODE_THREADS * (5 if access_token is None else 1)
    commit_language_chunks = await gather(
        funcs=[get_commits_languages for _ in node_id_chunks],
        args_dicts=[
            {
                "node_ids": node_id_chunk,
                "commit_repos": commit_repo_chunk,
                "repo_infos": repo_infos,
                "access_token": access_token,
            }
            for (node_id_chunk, commit_repo_chunk) in zip(
                node_id_chunks, commit_repo_chunks
            )
        ],
        max_threads=max_threads,
    )

    commit_languages: List[t_languages] = [[{} for _ in repo] for repo in commit_infos]
    for languages, node_ids in zip(commit_language_chunks, node_id_chunks):
        for language, node_id in zip(languages, node_ids):
            commit_languages[id_mapping[node_id][0]][id_mapping[node_id][1]] = language

    commit_times_dict: Dict[str, List[datetime]] = {}
    commit_languages_dict: Dict[str, t_languages] = {}
    for repo, times, languages in zip(repos, commit_times, commit_languages):
        commit_times_dict[repo] = times
        commit_languages_dict[repo] = languages

    def get_stats() -> Dict[str, Union[int, Dict[str, int]]]:
        return {
            "contribs_count": 0,
            "commits_count": 0,
            "issues_count": 0,
            "prs_count": 0,
            "reviews_count": 0,
            "repos_count": 0,
            "other_count": 0,
            "languages": {},
        }

    def get_lists() -> Dict[str, Any]:
        return {
            "commits": [],
            "issues": [],
            "prs": [],
            "reviews": [],
            "repos": [],
        }

    total_stats = get_stats()
    public_stats = get_stats()
    total: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"date": "", "weekday": 0, "stats": get_stats(), "lists": get_lists()}
    )
    public: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"date": "", "weekday": 0, "stats": get_stats(), "lists": get_lists()}
    )
    repo_stats: Dict[str, Dict[str, Union[int, Dict[str, int]]]] = defaultdict(
        get_stats
    )
    repositories: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(
        lambda: defaultdict(
            lambda: {
                "date": "",
                "weekday": 0,
                "stats": get_stats(),
                "lists": get_lists(),
            }
        )
    )

    for calendar_year in calendars:
        for week in calendar_year.weeks:
            for day in week.contribution_days:
                day_str = str(day.date)
                total[day_str]["date"] = day.date.isoformat()
                total[day_str]["weekday"] = day.weekday
                total[day_str]["stats"]["contribs_count"] = day.count
                total[day_str]["stats"]["other_count"] = day.count
                public[day_str]["date"] = day.date.isoformat()
                public[day_str]["weekday"] = day.weekday
                public[day_str]["stats"]["contribs_count"] = day.count
                public[day_str]["stats"]["other_count"] = day.count
                total_stats["contribs_count"] += day.count  # type: ignore
                total_stats["other_count"] += day.count  # type: ignore
                public_stats["contribs_count"] += day.count  # type: ignore
                public_stats["other_count"] += day.count  # type: ignore

    def update(date_str: str, repo: str, event: str, count: int):
        # update global counts for this event
        total[date_str]["stats"][event + "_count"] += count
        total[date_str]["stats"]["other_count"] -= count
        total_stats[event + "_count"] += count  # type: ignore
        total_stats["other_count"] -= count  # type: ignore
        is_private = repo_infos[repo].is_private
        if not is_private:
            public[date_str]["stats"][event + "_count"] += count
            public[date_str]["stats"]["other_count"] -= count
            public_stats[event + "_count"] += count  # type: ignore
            public_stats["other_count"] -= count  # type: ignore
        # update repo counts for this event
        repositories[repo][date_str]["stats"][event + "_count"] += count
        repositories[repo][date_str]["stats"]["contribs_count"] += count
        repo_stats[repo][event + "_count"] += count  # type: ignore
        repo_stats[repo]["contribs_count"] += count  # type: ignore

    def update_langs(
        date_str: str,
        repo: str,
        langs_list: t_languages,
    ):
        is_private = repo_infos[repo].is_private
        for langs in langs_list:
            for lang, lang_data in langs.items():
                stores = [
                    total[date_str]["stats"]["languages"],
                    total_stats["languages"],
                    repositories[repo][date_str]["stats"]["languages"],
                    repo_stats[repo]["languages"],
                ]
                if not is_private:
                    stores.append(public[date_str]["stats"]["languages"])
                    stores.append(public_stats["languages"])
                for store in stores:
                    if lang not in store:  # type: ignore
                        store[lang] = {"color": lang_data["color"], "additions": 0, "deletions": 0}  # type: ignore
                    store[lang]["additions"] += lang_data["additions"]  # type: ignore
                    store[lang]["deletions"] += lang_data["deletions"]  # type: ignore

    for events_year in all_events:
        for repo, repo_events in events_year.items():
            for event_type in ["commits", "issues", "prs", "reviews", "repos"]:
                events = sorted(repo_events[event_type], key=lambda x: x.occurred_at)
                for event in events:
                    datetime_obj = event.occurred_at.astimezone(tz)
                    date_str = datetime_obj.date().isoformat()
                    datetime_str = datetime_obj.isoformat()
                    repositories[repo][date_str]["date"] = date_str
                    if isinstance(event, RawEventsCommit):
                        commit_info: t_commits = []
                        langs_list: t_languages = []
                        count = 0
                        while len(commit_times_dict[repo]) > 0 and count < event.count:
                            raw_time = commit_times_dict[repo].pop(0)
                            langs = commit_languages_dict[repo].pop(0)
                            langs_list.append(langs)
                            time = pytz.utc.localize(raw_time).astimezone(tz)
                            commit_info.append(
                                {"timestamp": time.isoformat(), "languages": langs}
                            )
                            count += 1

                        # record timestamps
                        total[date_str]["lists"]["commits"].extend(commit_info)
                        repositories[repo][date_str]["lists"]["commits"].extend(
                            commit_info
                        )
                        if not repo_infos[repo].is_private:
                            public[date_str]["lists"]["commits"].extend(commit_info)

                        # update stats
                        update(date_str, repo, "commits", event.count)
                        update_langs(date_str, repo, langs_list)
                    else:
                        # record timestamps
                        total[date_str]["lists"][event_type].append(datetime_str)
                        repositories[repo][date_str]["lists"][event_type].append(
                            datetime_str
                        )
                        if not repo_infos[repo].is_private:
                            public[date_str]["lists"][event_type].append(datetime_str)

                        # update stats
                        update(date_str, repo, event_type, 1)

    total_list = list(
        filter(lambda x: x["stats"]["contribs_count"] > 0, list(total.values()))
    )
    public_list = list(
        filter(lambda x: x["stats"]["contribs_count"] > 0, list(public.values()))
    )
    repositories_list = {
        name: list(repo.values()) for name, repo in repositories.items()
    }

    for repo in repo_stats:
        repo_stats[repo]["private"] = repo_infos[repo].is_private

    cls = FullUserContributions if full else UserContributions
    output = cls.parse_obj(
        {
            "total_stats": total_stats,
            "public_stats": public_stats,
            "total": total_list,
            "public": public_list,
            "repo_stats": repo_stats,
            "repos": repositories_list,
        }
    )

    return output
