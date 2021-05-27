from datetime import datetime
from typing import Any, Dict, List

from external.github_api.rest.repo import get_repo_commits
from external.github_api.graphql.commit import get_commits


BLACKLIST = ["Jupyter Notebook"]
CUTOFF = 1000


def get_all_commit_info(
    user_id: str,
    name_with_owner: str,
    start_date: datetime = datetime.now(),
    end_date: datetime = datetime.now(),
) -> List[datetime]:
    """Gets all user's commit times for a given repository"""
    owner, repo = name_with_owner.split("/")
    data: List[Any] = []
    index = 0
    while index in range(10) and len(data) == 100 * index:
        data.extend(
            get_repo_commits(
                owner=owner,
                repo=repo,
                user=user_id,
                since=start_date,
                until=end_date,
                page=index + 1,
            )
        )
        index += 1

    data = list(
        map(
            lambda x: [
                datetime.strptime(
                    x["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ"
                ),
                x["node_id"],
            ],
            data,
        )
    )

    # sort ascending
    data = sorted(data, key=lambda x: x[0])
    return data


def get_commits_languages(
    node_ids: List[str], cutoff: int = CUTOFF
) -> List[Dict[str, Dict[str, int]]]:
    out: List[Dict[str, Dict[str, int]]] = []
    all_data: List[Dict[str, Any]] = []
    for i in range(0, len(node_ids), 100):
        # TODO: handle exception to get_commits
        # ideally would alert users somehow that data is incomplete
        try:
            raw_data = get_commits(node_ids[i : min(len(node_ids), i + 100)])
            data: List[Dict[str, Any]] = raw_data["data"]["nodes"]  # type: ignore
            all_data.extend(data)
        except Exception:
            print("Commit Exception")

    for commit in all_data:
        out.append({})
        if commit["additions"] + commit["deletions"] < cutoff:
            languages = [
                x
                for x in commit["repository"]["languages"]["edges"]
                if x["node"]["name"] not in BLACKLIST
            ]
            num_langs = min(len(languages), commit["changedFiles"])
            total_repo_size = sum(
                [language["size"] for language in languages[:num_langs]]
            )
            for language in languages[:num_langs]:
                lang_name = language["node"]["name"]
                additions = round(
                    commit["additions"] * language["size"] / total_repo_size
                )
                deletions = round(
                    commit["deletions"] * language["size"] / total_repo_size
                )
                if additions > 0 or deletions > 0:
                    out[-1][lang_name] = {
                        "additions": additions,
                        "deletions": deletions,
                    }

    return out
