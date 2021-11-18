from datetime import datetime
from typing import Dict, List, Optional, Union

from src.constants import (
    BLACKLIST,
    CUTOFF,
    CUTOFF_PER_FILE,
    DEFAULT_COLOR,
    NODE_CHUNK_SIZE,
)
from src.data.github.graphql import RawCommit as GraphQLRawCommit, RawRepo, get_commits
from src.data.github.rest import RawCommit as RESTRawCommit, get_repo_commits


def get_all_commit_info(
    user_id: str,
    name_with_owner: str,
    start_date: datetime,
    end_date: datetime,
    access_token: Optional[str] = None,
) -> List[RESTRawCommit]:
    """Gets all user's commit times for a given repository"""
    owner, repo = name_with_owner.split("/")
    data: List[RESTRawCommit] = []

    def _get_repo_commits(page: int):
        return get_repo_commits(
            owner, repo, user_id, start_date, end_date, page, access_token
        )

    for i in range(10):
        if len(data) == 100 * i:
            data.extend(_get_repo_commits(i + 1))

    # sort ascending
    sorted_data = sorted(data, key=lambda x: x.timestamp)
    return sorted_data


def _get_commits_languages(
    node_ids: List[str],
    per_page: int = NODE_CHUNK_SIZE,
    access_token: Optional[str] = None,
) -> List[Optional[GraphQLRawCommit]]:
    all_data: List[Optional[GraphQLRawCommit]] = []
    for i in range(0, len(node_ids), per_page):
        cutoff = min(len(node_ids), i + per_page)
        all_data.extend(get_commits(node_ids[i:cutoff], access_token))
    return all_data


def get_commits_languages(
    node_ids: List[str],
    commit_repos: List[str],
    repo_infos: Dict[str, RawRepo],
    cutoff: int = CUTOFF,
    cutoff_per_file: int = CUTOFF_PER_FILE,
    access_token: Optional[str] = None,
):
    all_data = _get_commits_languages(
        node_ids, per_page=NODE_CHUNK_SIZE, access_token=access_token
    )

    out: List[Dict[str, Dict[str, Union[int, str]]]] = []
    for commit, commit_repo in zip(all_data, commit_repos):
        out.append({})
        if commit is None:
            continue

        loc_changed = commit.additions + commit.deletions
        loc_changed_per_file = loc_changed / max(1, commit.changed_files)
        if loc_changed < cutoff or loc_changed_per_file < cutoff_per_file:
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
                        "color": lang_color or DEFAULT_COLOR,
                    }

    return out
