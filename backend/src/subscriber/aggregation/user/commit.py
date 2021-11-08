from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from src.data.github.graphql import get_commits, RawCommit, RawRepo
from src.data.github.rest import get_repo_commits
from src.constants import NODE_CHUNK_SIZE, CUTOFF, BLACKLIST


def get_all_commit_info(
    user_id: str,
    access_token: str,
    name_with_owner: str,
    start_date: datetime = datetime.now(),
    end_date: datetime = datetime.now(),
) -> List[Tuple[datetime, Any]]:
    """Gets all user's commit times for a given repository"""
    owner, repo = name_with_owner.split("/")
    data: List[Any] = []
    index = 0
    while index < 10 and len(data) == 100 * index:
        data.extend(
            get_repo_commits(
                access_token=access_token,
                owner=owner,
                repo=repo,
                user=user_id,
                since=start_date,
                until=end_date,
                page=index + 1,
            )
        )
        index += 1

    def extract_info(x: Any) -> Tuple[datetime, Any]:
        return (
            datetime.strptime(x["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ"),
            x["node_id"],
        )

    extracted_data = list(map(extract_info, data))

    # sort ascending
    sorted_data = sorted(extracted_data, key=lambda x: x[0])
    return sorted_data


def _get_commits_languages(
    access_token: str, node_ids: List[str], per_page: int = NODE_CHUNK_SIZE
) -> List[Optional[RawCommit]]:
    all_data: List[Optional[RawCommit]] = []
    for i in range(0, len(node_ids), per_page):
        cutoff = min(len(node_ids), i + per_page)
        all_data.extend(get_commits(access_token, node_ids[i:cutoff]))
    return all_data


def get_commits_languages(
    access_token: str,
    node_ids: List[str],
    commit_repos: List[str],
    repo_infos: Dict[str, RawRepo],
    cutoff: int = CUTOFF,
):
    all_data = _get_commits_languages(access_token, node_ids, per_page=NODE_CHUNK_SIZE)

    out: List[Dict[str, Dict[str, Union[int, str]]]] = []
    for commit, commit_repo in zip(all_data, commit_repos):
        out.append({})
        if commit is not None and commit.additions + commit.deletions < cutoff:
            repo_info = repo_infos[commit_repo].languages.edges
            languages = [x for x in repo_info if x.node.name not in BLACKLIST]
            total_repo_size = sum([language.size for language in languages])
            for language in languages:
                lang_name = language.node.name
                lang_color = language.node.color
                lang_size = language.size
                additions = round(commit.additions * lang_size / total_repo_size)
                deletions = round(commit.deletions * lang_size / total_repo_size)
                if additions > 0 or deletions > 0:
                    out[-1][lang_name] = {
                        "additions": additions,
                        "deletions": deletions,
                        "color": lang_color,
                    }

    return out
