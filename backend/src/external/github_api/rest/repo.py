from datetime import datetime
from typing import Any, Dict, List, Optional

from src.external.github_api.rest.template import (
    RESTErrorEmptyRepo,
    get_template,
    get_template_plural,
)

BASE_URL = "https://api.github.com/repos/"


# TODO: create return classes


def get_repo(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """Returns raw repository data"""
    return get_template(BASE_URL + owner + "/" + repo, access_token)


def get_repo_languages(
    access_token: str, owner: str, repo: str
) -> List[Dict[str, Any]]:
    """Returns repository language breakdown"""
    return get_template_plural(
        BASE_URL + owner + "/" + repo + "/languages", access_token
    )


def get_repo_stargazers(
    access_token: str, owner: str, repo: str, per_page: int = 100
) -> List[Dict[str, Any]]:
    """Returns stargazers with timestamp for repository"""
    return get_template_plural(
        BASE_URL + owner + "/" + repo + "/stargazers",
        access_token,
        per_page=per_page,
        accept_header="applicaiton/vnd.github.v3.star+json",
    )


# does not accept per page, exceeds if necessary
def get_repo_code_frequency(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """Returns code frequency for repository"""
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/code_frequency", access_token
    )


def get_repo_commit_activity(
    access_token: str, owner: str, repo: str
) -> Dict[str, Any]:
    """Returns commit activity for past year, broken by week"""
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/commit_activity", access_token
    )


def get_repo_contributors(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """Returns contributors for a repository"""
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/contributors", access_token
    )


def get_repo_weekly_commits(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """Returns contributions by week, owner/non-owner"""
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/participation", access_token
    )


def get_repo_hourly_commits(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """Returns contributions by day, hour for repository"""
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/punch_card", access_token
    )


def get_repo_commits(
    access_token: str,
    owner: str,
    repo: str,
    user: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    page: int = 1,
) -> List[Dict[str, Any]]:
    """Returns most recent commits including commit message"""
    user = user if user is not None else owner
    query = BASE_URL + owner + "/" + repo + "/commits?author=" + user
    if since is not None:
        query += "&since=" + str(since)
    if until is not None:
        query += "&until=" + str(until)
    try:
        return get_template_plural(query, access_token, page=page)
    except RESTErrorEmptyRepo:
        return []
