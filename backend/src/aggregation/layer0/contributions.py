from collections import defaultdict
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import pytz

from src.aggregation.layer0.languages import CommitLanguages, get_commit_languages
from src.constants import (
    GRAPHQL_NODE_CHUNK_SIZE,
    GRAPHQL_NODE_THREADS,
    NODE_QUERIES,
    PR_FILES,
    REST_NODE_THREADS,
)
from src.data.github.graphql import (
    RawCalendar,
    RawCommit as GraphQLRawCommit,
    RawEventsCommit,
    RawEventsEvent,
    RawRepo,
    get_commits,
    get_repo,
    get_user_contribution_calendar,
    get_user_contribution_events,
)
from src.data.github.rest import (
    RawCommit as RESTRawCommit,
    RawCommitFile,
    get_commit_files,
    get_repo_commits,
)
from src.models import UserContributions
from src.utils import date_to_datetime, gather


class ContribsList:
    def __init__(self):
        self.commits: List[RawEventsCommit] = []
        self.issues: List[RawEventsEvent] = []
        self.prs: List[RawEventsEvent] = []
        self.reviews: List[RawEventsEvent] = []
        self.repos: List[RawEventsEvent] = []

    def add(self, label: str, event: Union[RawEventsCommit, RawEventsEvent]):
        if label == "commit" and isinstance(event, RawEventsCommit):
            self.commits.append(event)
        elif label == "issue" and isinstance(event, RawEventsEvent):
            self.issues.append(event)
        elif label == "pr" and isinstance(event, RawEventsEvent):
            self.prs.append(event)
        elif label == "review" and isinstance(event, RawEventsEvent):
            self.reviews.append(event)
        elif label == "repo" and isinstance(event, RawEventsEvent):
            self.repos.append(event)


def get_user_all_contribution_events(
    user_id: str,
    start_date: datetime,
    end_date: datetime,
    access_token: Optional[str] = None,
) -> Dict[str, ContribsList]:
    repo_contribs: Dict[str, ContribsList] = defaultdict(lambda: ContribsList())
    after: Optional[str] = ""
    cont = True
    while cont:
        after_str = after if isinstance(after, str) else ""
        response = get_user_contribution_events(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            after=after_str,
            access_token=access_token,
        )

        cont = False
        node_lists = [
            ("commit", response.commit_contribs_by_repo),
            ("issue", response.issue_contribs_by_repo),
            ("pr", response.pr_contribs_by_repo),
            ("review", response.review_contribs_by_repo),
        ]
        for event_type, event_list in node_lists:
            for repo in event_list:
                name = repo.repo.name
                for event in repo.contribs.nodes:
                    repo_contribs[name].add(event_type, event)
                if repo.contribs.page_info.has_next_page:
                    after = repo.contribs.page_info.end_cursor
                    cont = True

        for repo in response.repo_contribs.nodes:
            name = repo.repo.name
            node = RawEventsEvent(occurredAt=repo.occurred_at)
            repo_contribs[name].add("repo", node)

    return repo_contribs


def get_all_commit_info(
    user_id: str,
    name_with_owner: str,
    start_date: datetime,
    end_date: datetime,
    access_token: Optional[str] = None,
) -> List[RESTRawCommit]:
    owner, repo = name_with_owner.split("/")
    data: List[RESTRawCommit] = []
    for i in range(10):
        if len(data) == 100 * i:
            new_data = get_repo_commits(
                owner, repo, user_id, start_date, end_date, i + 1, access_token
            )
            data.extend(new_data)

    # sort ascending
    return sorted(data, key=lambda x: x.timestamp)


async def get_all_commit_languages(
    commit_infos: List[List[RESTRawCommit]],
    repos: List[str],
    repo_infos: Dict[str, RawRepo],
    access_token: Optional[str] = None,
    catch_errors: bool = False,
) -> Tuple[Dict[str, List[datetime]], Dict[str, List[CommitLanguages]]]:
    commit_node_ids = [[x.node_id for x in repo] for repo in commit_infos]
    commit_times = [[x.timestamp for x in repo] for repo in commit_infos]

    id_mapping: Dict[str, Tuple[int, int]] = {}
    repo_mapping: Dict[str, str] = {}
    all_node_ids: List[str] = []
    for i, repo_node_ids in enumerate(commit_node_ids):
        for j, node_id in enumerate(repo_node_ids):
            id_mapping[node_id] = (i, j)
            repo_mapping[node_id] = repos[i]
            all_node_ids.append(node_id)

    node_id_chunks: List[List[str]] = [
        all_node_ids[i : min(len(all_node_ids), i + GRAPHQL_NODE_CHUNK_SIZE)]
        for i in range(0, len(all_node_ids), GRAPHQL_NODE_CHUNK_SIZE)
    ]

    commit_language_chunks: List[List[Optional[GraphQLRawCommit]]] = await gather(
        funcs=[get_commits for _ in node_id_chunks],
        args_dicts=[
            {
                "node_ids": node_id_chunk,
                "access_token": access_token,
                "catch_errors": catch_errors,
            }
            for node_id_chunk in node_id_chunks
        ],
        max_threads=GRAPHQL_NODE_THREADS,
    )

    temp_commit_languages: List[Optional[GraphQLRawCommit]] = []
    for commit_language_chunk in commit_language_chunks:
        temp_commit_languages.extend(commit_language_chunk)

    # returns commits with no associated PR or incomplete PR
    filtered_commits: List[GraphQLRawCommit] = filter(
        lambda x: x is not None
        and (len(x.prs.nodes) == 0 or x.prs.nodes[0].changed_files > PR_FILES)
        and (x.additions + x.deletions > 100),
        temp_commit_languages,
    )  # type: ignore

    # get NODE_QUERIES largest commits with no associated PR or incomplete PR
    sorted_commits = sorted(
        filtered_commits, key=lambda x: x.additions + x.deletions, reverse=True
    )[:NODE_QUERIES]

    sorted_commit_urls = [commit.url.split("/") for commit in sorted_commits]
    commit_files: List[List[RawCommitFile]] = await gather(
        funcs=[get_commit_files for _ in sorted_commit_urls],
        args_dicts=[
            {
                "owner": url[3],
                "repo": url[4],
                "sha": url[6],
                "access_token": access_token,
            }
            for url in sorted_commit_urls
        ],
        max_threads=REST_NODE_THREADS,
    )

    commit_files_dict: Dict[str, List[RawCommitFile]] = {
        commit.url: commit_file
        for commit, commit_file in zip(sorted_commits, commit_files)
    }

    commit_languages: List[List[CommitLanguages]] = [
        [CommitLanguages() for _ in repo] for repo in commit_infos
    ]
    for raw_commits, node_ids in zip(commit_language_chunks, node_id_chunks):
        for raw_commit, node_id in zip(raw_commits, node_ids):
            curr_commit_files: Optional[List[RawCommitFile]] = None
            if raw_commit is not None and raw_commit.url in commit_files_dict:
                curr_commit_files = commit_files_dict[raw_commit.url]
            lang_breakdown = get_commit_languages(
                raw_commit, curr_commit_files, repo_infos[repo_mapping[node_id]]
            )
            i, j = id_mapping[node_id]
            commit_languages[i][j] = lang_breakdown

    commit_times_dict: Dict[str, List[datetime]] = {}
    commit_languages_dict: Dict[str, List[CommitLanguages]] = {}
    for repo, times, languages in zip(repos, commit_times, commit_languages):
        commit_times_dict[repo] = times
        commit_languages_dict[repo] = languages

    return commit_times_dict, commit_languages_dict


async def get_cleaned_contributions(
    user_id: str,
    start_date: datetime,
    end_date: datetime,
    access_token: Optional[str],
    catch_errors: bool = False,
) -> Tuple[
    RawCalendar,
    Dict[str, ContribsList],
    Dict[str, RawRepo],
    Dict[str, List[datetime]],
    Dict[str, List[CommitLanguages]],
]:
    calendar = get_user_contribution_calendar(
        user_id, start_date, end_date, access_token
    )
    contrib_events = get_user_all_contribution_events(
        user_id, start_date, end_date, access_token
    )
    repos: List[str] = list(set(contrib_events.keys()))

    commit_infos: List[List[RESTRawCommit]] = await gather(
        funcs=[get_all_commit_info for _ in repos],
        args_dicts=[
            {
                "user_id": user_id,
                "name_with_owner": repo,
                "start_date": start_date,
                "end_date": end_date,
                "access_token": access_token,
            }
            for repo in repos
        ],
        max_threads=REST_NODE_THREADS,
    )

    _repo_infos: List[Optional[RawRepo]] = await gather(
        funcs=[get_repo for _ in repos],
        args_dicts=[
            {
                "owner": repo.split("/")[0],
                "repo": repo.split("/")[1],
                "access_token": access_token,
                "catch_errors": catch_errors,
            }
            for repo in repos
        ],
        max_threads=REST_NODE_THREADS,
    )

    repo_infos = {k: v for k, v in zip(repos, _repo_infos) if v is not None}

    commit_times_dict, commit_languages_dict = await get_all_commit_languages(
        commit_infos,
        repos,
        repo_infos,
        access_token,
        catch_errors,
    )

    return (
        calendar,
        contrib_events,
        repo_infos,
        commit_times_dict,
        commit_languages_dict,
    )


class StatsContainer:
    def __init__(self):
        self.contribs: int = 0
        self.commits: int = 0
        self.issues: int = 0
        self.prs: int = 0
        self.reviews: int = 0
        self.repos: int = 0
        self.other: int = 0
        self.languages = CommitLanguages()

    def add_stat(self, label: str, count: int, add: bool = False) -> None:
        if label == "commit":
            self.commits += count
        elif label == "issue":
            self.issues += count
        elif label == "pr":
            self.prs += count
        elif label == "review":
            self.reviews += count
        elif label == "repo":
            self.repos += count

        if add:
            self.contribs += count
        else:
            self.other -= count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contribs_count": self.contribs,
            "commits_count": self.commits,
            "issues_count": self.issues,
            "prs_count": self.prs,
            "reviews_count": self.reviews,
            "repos_count": self.repos,
            "other_count": self.other,
            "languages": self.languages.to_dict(),
        }


class ListsContainer:
    def __init__(self):
        self.commits: List[datetime] = []
        self.issues: List[datetime] = []
        self.prs: List[datetime] = []
        self.reviews: List[datetime] = []
        self.repos: List[datetime] = []

    def add_list(self, label: str, times: List[datetime]) -> None:
        if label == "commit":
            self.commits.extend(times)
        elif label == "issue":
            self.issues.extend(times)
        elif label == "pr":
            self.prs.extend(times)
        elif label == "review":
            self.reviews.extend(times)
        elif label == "repo":
            self.repos.extend(times)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "commits": self.commits,
            "issues": self.issues,
            "prs": self.prs,
            "reviews": self.reviews,
            "repos": self.repos,
        }


class DateContainer:
    def __init__(self):
        self.date = ""
        self.weekday = 0
        self.stats = StatsContainer()
        self.lists = ListsContainer()

    def add_stat(
        self, label: str, count: int, times: List[datetime], add: bool = False
    ):
        self.stats.add_stat(label, count, add)
        self.lists.add_list(label, times)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "weekday": self.weekday,
            "stats": self.stats.to_dict(),
            "lists": self.lists.to_dict(),
        }


# assumed one month span, can be no more than one year
async def get_contributions(
    user_id: str,
    start_date: date,
    end_date: date,
    timezone_str: str = "US/Eastern",
    access_token: Optional[str] = None,
    catch_errors: bool = False,
) -> UserContributions:
    tz = pytz.timezone(timezone_str)

    start_month = date_to_datetime(start_date)
    end_month = date_to_datetime(end_date, hour=23, minute=59, second=59)
    (
        calendar,
        contrib_events,
        repo_infos,
        commit_times_dict,
        commit_languages_dict,
    ) = await get_cleaned_contributions(
        user_id, start_month, end_month, access_token, catch_errors
    )

    total_stats = StatsContainer()
    public_stats = StatsContainer()
    total: Dict[str, DateContainer] = defaultdict(DateContainer)
    public: Dict[str, DateContainer] = defaultdict(DateContainer)
    repo_stats: Dict[str, StatsContainer] = defaultdict(StatsContainer)
    repositories: Dict[str, Dict[str, DateContainer]] = defaultdict(
        lambda: defaultdict(DateContainer)
    )

    for week in calendar.weeks:
        for day in week.contribution_days:
            day_str = str(day.date)
            for obj, stats_obj in [(total, total_stats), (public, public_stats)]:
                obj[day_str].date = day.date.isoformat()
                obj[day_str].weekday = day.weekday
                obj[day_str].stats.contribs = day.count
                obj[day_str].stats.other = day.count
                stats_obj.contribs += day.count
                stats_obj.other += day.count

    def update_stats(
        date_str: str, repo: str, event: str, count: int, times: List[datetime]
    ):
        # update global counts for this event
        total[date_str].add_stat(event, count, times)
        total_stats.add_stat(event, count)
        if not repo_infos[repo].is_private:
            public[date_str].add_stat(event, count, times)
            public_stats.add_stat(event, count)
        repositories[repo][date_str].add_stat(event, count, times, add=True)
        repo_stats[repo].add_stat(event, count, add=True)

    def update_langs(date_str: str, repo: str, langs: CommitLanguages):
        stores = [
            total[date_str].stats.languages,
            total_stats.languages,
            repositories[repo][date_str].stats.languages,
            repo_stats[repo].languages,
        ]
        if not repo_infos[repo].is_private:
            stores.append(public[date_str].stats.languages)
            stores.append(public_stats.languages)

        for store in stores:
            store += langs

    for repo, repo_events in contrib_events.items():
        for label, events in [
            ("commit", repo_events.commits),
            ("issue", repo_events.issues),
            ("pr", repo_events.prs),
            ("review", repo_events.reviews),
            ("repo", repo_events.repos),
        ]:
            events = sorted(events, key=lambda x: x.occurred_at)
            for event in events:
                datetime_obj = event.occurred_at.astimezone(tz)
                date_str = datetime_obj.date().isoformat()
                repositories[repo][date_str].date = date_str
                if isinstance(event, RawEventsCommit):
                    count = 0
                    commit_times: List[datetime] = []
                    while len(commit_languages_dict[repo]) > 0 and count < event.count:
                        commit_times.append(commit_times_dict[repo].pop(0))
                        langs = commit_languages_dict[repo].pop(0)
                        update_langs(date_str, repo, langs)
                        count += 1
                    update_stats(date_str, repo, "commit", event.count, commit_times)
                else:
                    update_stats(date_str, repo, label, 1, [datetime_obj])

    total_stats_dict = total_stats.to_dict()
    public_stats_dict = public_stats.to_dict()
    repo_stats_dict = {name: stats.to_dict() for name, stats in repo_stats.items()}

    for repo in repo_stats:
        repo_stats_dict[repo]["private"] = repo_infos[repo].is_private

    total_list = [v.to_dict() for v in total.values() if v.stats.contribs > 0]
    public_list = [v.to_dict() for v in public.values() if v.stats.contribs > 0]
    repositories_list = {
        name: [v.to_dict() for v in repo.values()]
        for name, repo in repositories.items()
    }

    output = UserContributions.model_validate(
        {
            "total_stats": total_stats_dict,
            "public_stats": public_stats_dict,
            "total": total_list,
            "public": public_list,
            "repo_stats": repo_stats_dict,
            "repos": repositories_list,
        }
    )

    return output
