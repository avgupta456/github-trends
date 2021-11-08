from datetime import datetime
from typing import Dict, List, Optional, Union

from src.data.github.graphql import get_commits, RawRepo, RawCommit as GraphQLRawCommit
from src.data.github.rest import get_repo_commits, RawCommit as RESTRawCommit
from src.constants import NODE_CHUNK_SIZE, CUTOFF, BLACKLIST


def get_all_commit_info(
    user_id: str,
    access_token: str,
    name_with_owner: str,
    start_date: datetime,
    end_date: datetime,
) -> List[RESTRawCommit]:
    """Gets all user's commit times for a given repository"""
    owner, repo = name_with_owner.split("/")
    data: List[RESTRawCommit] = []

    def _get_repo_commits(page: int):
        return get_repo_commits(
            access_token, owner, repo, user_id, start_date, end_date, page
        )

    for i in range(10):
        if len(data) == 100 * i:
            data.extend(_get_repo_commits(i + 1))

    # sort ascending
    sorted_data = sorted(data, key=lambda x: x.timestamp)
    return sorted_data


def _get_commits_languages(
    access_token: str, node_ids: List[str], per_page: int = NODE_CHUNK_SIZE
) -> List[Optional[GraphQLRawCommit]]:
    all_data: List[Optional[GraphQLRawCommit]] = []
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
