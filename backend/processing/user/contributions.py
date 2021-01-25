from collections import defaultdict
from datetime import date, timedelta
from typing import Any, DefaultDict, Dict, List, Optional, Union

from external.github_api.graphql.user import (get_user_contribution_calendar,
                                              get_user_contribution_events,
                                              get_user_contribution_years)
from helper.gather import gather
from models.user.contribs import (RawCalendar, RawEventsCommit, RawEventsEvent,
                                  UserContributions)
from pytz import timezone

t = DefaultDict[str, Dict[str, List[Union[RawEventsEvent, RawEventsCommit]]]]


# TODO: handle more timezones
eastern = timezone("US/Eastern")


def get_user_all_contribution_events(
    user_id: str,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
) -> t:
    repo_contribs: t = defaultdict(
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
) -> UserContributions:

    # get years for contribution calendar
    years = list(
        filter(
            lambda x: start_date.year <= x <= end_date.year,
            get_user_contribution_years(user_id),
        )
    )

    # async get contribution calendars
    calendars: List[RawCalendar] = gather(
        funcs=[get_user_contribution_calendar for _ in years],
        args_dicts=[
            {
                "user_id": user_id,
                "start_date": max(date(year, 1, 1), start_date),
                "end_date": min(date(year, 12, 31), end_date),
            }
            for year in years
        ],
    )

    events: List[t] = gather(
        funcs=[get_user_all_contribution_events for _ in years],
        args_dicts=[
            {
                "user_id": user_id,
                "start_date": max(date(year, 1, 1), start_date),
                "end_date": min(date(year, 12, 31), end_date),
            }
            for year in years
        ],
    )

    # TODO: Supplement with commit times

    repos = set()
    for events_year in events:
        for repo in events_year:
            repos.add(repo)
    repos = list(repos)

    def get_stats():
        return {
            "contribs_count": 0,
            "commits_count": 0,
            "issues_count": 0,
            "prs_count": 0,
            "reviews_count": 0,
            "repos_count": 0,
            "other_count": 0,
        }

    def get_lists():
        return {
            "commits": [],
            "issues": [],
            "prs": [],
            "reviews": [],
            "repos": [],
        }

    total_stats: Dict[str, int] = get_stats()
    total: DefaultDict[str, Dict[str, Any]] = defaultdict(
        lambda: {"date": "", "weekday": 0, "stats": get_stats(), "lists": get_lists()}
    )
    repo_stats: DefaultDict[str, Dict[str, int]] = defaultdict(lambda: get_stats())
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
                total_stats["contribs_count"] += day.count
                total_stats["other_count"] += day.count

    for events_year in events:
        for repo, repo_events in events_year.items():
            for event_type in ["commits", "issues", "prs", "reviews", "repos"]:
                for event in repo_events[event_type]:
                    datetime_obj = event.occurred_at.astimezone(eastern)
                    date_str = str(datetime_obj.date())
                    if isinstance(event, RawEventsCommit):
                        total[date_str]["stats"]["commits_count"] += event.count
                        total_stats["commits_count"] += event.count
                        repositories[repo][date_str]["stats"][
                            "commits_count"
                        ] += event.count
                        repo_stats[repo]["commits_count"] += event.count
                        total[date_str]["stats"]["other_count"] -= event.count
                        total_stats["other_count"] -= event.count
                        repositories[repo][date_str]["stats"][
                            "contribs_count"
                        ] += event.count
                        repo_stats[repo]["contribs_count"] += event.count
                    else:
                        total[date_str]["stats"][event_type + "_count"] += 1
                        total_stats[event_type + "_count"] += 1
                        repositories[repo][date_str]["stats"][
                            event_type + "_count"
                        ] += 1
                        repo_stats[repo][event_type + "_count"] += 1
                        total[date_str]["lists"][event_type].append(datetime_obj)
                        repositories[repo][date_str]["lists"][event_type].append(
                            datetime_obj
                        )
                        total[date_str]["stats"]["other_count"] -= 1
                        total_stats["other_count"] -= 1
                        repositories[repo][date_str]["stats"]["contribs_count"] += 1
                        repo_stats[repo]["contribs_count"] += 1

                    repositories[repo][date_str]["date"] = datetime_obj.date()

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
