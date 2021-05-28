from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any, DefaultDict, Dict, List, Optional, Set, Union

import pytz
from pytz import timezone

from models.user.contribs import (
    RawCalendar,
    RawEventsCommit,
    RawEventsEvent,
    UserContributions,
)

from external.github_api.graphql.user import (
    get_user_contribution_years,
    get_user_contribution_calendar,
    get_user_contribution_events,
)

from helper.gather import gather

from utils import date_to_datetime
from constants import NODE_CHUNK_SIZE, NODE_THREADS

from processing.commit import get_all_commit_info, get_commits_languages

t_stats = DefaultDict[str, Dict[str, List[Union[RawEventsEvent, RawEventsCommit]]]]
t_commits = List[Dict[str, Union[Dict[str, Dict[str, int]], datetime]]]


def get_user_all_contribution_events(
    user_id: str,
    start_date: datetime = datetime.now() - timedelta(365),
    end_date: datetime = datetime.now(),
) -> t_stats:
    repo_contribs: t_stats = defaultdict(
        lambda: {"commits": [], "issues": [], "prs": [], "reviews": [], "repos": []}
    )
    after: Optional[str] = ""
    index, cont = 0, True
    while index < 10 and cont:
        after_str = after if isinstance(after, str) else ""
        response = get_user_contribution_events(
            user_id=user_id, start_date=start_date, end_date=end_date, after=after_str
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


def get_contributions(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
    timezone_str: str = "US/Eastern",
) -> UserContributions:
    tz = timezone(timezone_str)

    # get years for contribution calendar
    years = sorted(
        filter(
            lambda x: start_date.year <= x <= end_date.year,
            get_user_contribution_years(user_id),
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
    calendars: List[RawCalendar] = gather(
        funcs=[get_user_contribution_calendar for _ in years],
        args_dicts=[
            {
                "user_id": user_id,
                "start_date": dates[i][0],
                "end_date": dates[i][1],
            }
            for i in range(len(years))
        ],
    )

    all_events: List[t_stats] = gather(
        funcs=[get_user_all_contribution_events for _ in years],
        args_dicts=[
            {
                "user_id": user_id,
                "start_date": dates[i][0],
                "end_date": dates[i][1],
            }
            for i in range(len(years))
        ],
    )

    repos_set: Set[str] = set()
    for events_year in all_events:
        for repo in events_year:
            repos_set.add(repo)
    repos = list(repos_set)

    commit_infos = gather(
        funcs=[get_all_commit_info for _ in repos],
        args_dicts=[
            {
                "user_id": user_id,
                "name_with_owner": repo,
                "start_date": dates[0][0],  # first start
                "end_date": dates[-1][1],  # last end
            }
            for repo in repos
        ],
        max_threads=100,
    )

    commit_times = [[commit_info[0] for commit_info in repo] for repo in commit_infos]
    commit_node_ids = [
        [commit_info[1] for commit_info in repo] for repo in commit_infos
    ]

    id_mapping: Dict[str, List[int]] = {}
    all_node_ids: List[str] = []
    for i, repo_node_ids in enumerate(commit_node_ids):
        for j, node_id in enumerate(repo_node_ids):
            id_mapping[node_id] = [i, j]
            all_node_ids.append(node_id)

    node_id_chunks: List[List[str]] = []
    for i in range(0, len(all_node_ids), NODE_CHUNK_SIZE):
        node_id_chunks.append(
            all_node_ids[i : min(len(all_node_ids), i + NODE_CHUNK_SIZE)]
        )

    commit_language_chunks = gather(
        funcs=[get_commits_languages for _ in node_id_chunks],
        args_dicts=[{"node_ids": node_id_chunk} for node_id_chunk in node_id_chunks],
        max_threads=NODE_THREADS,
    )

    commit_languages: List[List[Dict[str, Dict[str, int]]]] = [
        [{} for _ in repo] for repo in commit_infos
    ]
    for languages, node_ids in zip(commit_language_chunks, node_id_chunks):
        for language, node_id in zip(languages, node_ids):
            commit_languages[id_mapping[node_id][0]][id_mapping[node_id][1]] = language

    commit_times_dict: Dict[str, List[datetime]] = {}
    commit_languages_dict: Dict[str, List[Dict[str, Dict[str, int]]]] = {}
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
    total: DefaultDict[str, Dict[str, Any]] = defaultdict(
        lambda: {"date": "", "weekday": 0, "stats": get_stats(), "lists": get_lists()}
    )
    repo_stats: DefaultDict[str, Dict[str, Union[int, Dict[str, int]]]] = defaultdict(
        get_stats
    )
    repositories: DefaultDict[str, DefaultDict[str, Dict[str, Any]]] = defaultdict(
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
                total[str(day.date)]["date"] = day.date
                total[str(day.date)]["weekday"] = day.weekday
                total[str(day.date)]["stats"]["contribs_count"] = day.count
                total[str(day.date)]["stats"]["other_count"] = day.count
                total_stats["contribs_count"] += day.count  # type: ignore
                total_stats["other_count"] += day.count  # type: ignore

    def update(date_str: str, repo: str, event: str, count: int):
        # update global counts for this event
        total[date_str]["stats"][event + "_count"] += count
        total_stats[event + "_count"] += count  # type: ignore
        # update repo counts for this event
        repositories[repo][date_str]["stats"][event + "_count"] += count
        repo_stats[repo][event + "_count"] += count  # type: ignore
        # update total other stats by subtracting
        total[date_str]["stats"]["other_count"] -= count
        total_stats["other_count"] -= count  # type: ignore
        # update repo total stats by adding
        repositories[repo][date_str]["stats"]["contribs_count"] += count
        repo_stats[repo]["contribs_count"] += count  # type: ignore

    def update_langs(
        date_str: str, repo: str, langs_list: List[Dict[str, Dict[str, int]]]
    ):
        for langs in langs_list:
            for lang, lang_data in langs.items():
                for store in [
                    total[date_str]["stats"]["languages"],
                    total_stats["languages"],
                    repositories[repo][date_str]["stats"]["languages"],
                    repo_stats[repo]["languages"],
                ]:
                    if lang not in store:  # type: ignore
                        store[lang] = {"additions": 0, "deletions": 0}  # type: ignore
                    store[lang]["additions"] += lang_data["additions"]  # type: ignore
                    store[lang]["deletions"] += lang_data["deletions"]  # type: ignore

    for events_year in all_events:
        for repo, repo_events in events_year.items():
            for event_type in ["commits", "issues", "prs", "reviews", "repos"]:
                events = sorted(repo_events[event_type], key=lambda x: x.occurred_at)
                for event in events:
                    datetime_obj = event.occurred_at.astimezone(tz)
                    date_str = str(datetime_obj.date())
                    repositories[repo][date_str]["date"] = datetime_obj.date()
                    if isinstance(event, RawEventsCommit):
                        commit_info: t_commits = []
                        langs_list: List[Dict[str, Dict[str, int]]] = []
                        count = 0
                        while len(commit_times_dict[repo]) > 0 and count < event.count:
                            raw_time = commit_times_dict[repo].pop(0)
                            langs = commit_languages_dict[repo].pop(0)
                            langs_list.append(langs)
                            time = pytz.utc.localize(raw_time).astimezone(tz)
                            commit_info.append({"timestamp": time, "languages": langs})
                            count += 1

                        # record timestamps
                        total[date_str]["lists"]["commits"].extend(commit_info)
                        repositories[repo][date_str]["lists"]["commits"].extend(
                            commit_info
                        )

                        # update stats
                        update(date_str, repo, "commits", event.count)
                        update_langs(date_str, repo, langs_list)
                    else:
                        # update stats
                        update(date_str, repo, event_type, 1)

                        # record timestamps
                        total[date_str]["lists"][event_type].append(datetime_obj)
                        repositories[repo][date_str]["lists"][event_type].append(
                            datetime_obj
                        )

    total_list = list(total.values())
    repositories_list = {
        name: list(repo.values()) for name, repo in repositories.items()
    }

    output = UserContributions.parse_obj(
        {
            "total_stats": total_stats,
            "total": total_list,
            "repo_stats": repo_stats,
            "repos": repositories_list,
        }
    )

    return output
