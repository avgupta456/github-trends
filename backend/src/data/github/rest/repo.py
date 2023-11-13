import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.data.github.rest.models import RawCommit
from src.data.github.rest.template import RESTError, get_template, get_template_plural

BASE_URL = "https://api.github.com/repos/"


# NOTE: unused, untested
def get_repo(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """
    Returns raw repository data
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    :return: repository data
    """
    return get_template(BASE_URL + owner + "/" + repo, access_token)


# NOTE: unused, untested
def get_repo_languages(
    access_token: str, owner: str, repo: str
) -> List[Dict[str, Any]]:
    """
    Returns repository language breakdown
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    :return: repository language breakdown
    """
    return get_template_plural(
        BASE_URL + owner + "/" + repo + "/languages", access_token
    )


def get_repo_stargazers(
    access_token: str, owner: str, repo: str, per_page: int = 100, page: int = 1
) -> List[Dict[str, Any]]:
    """
    Returns stargazers with timestamp for repository
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    :param per_page: number of items per page
    :param page: page number
    :return: stargazers with timestamp for repository
    """
    return get_template_plural(
        BASE_URL + owner + "/" + repo + "/stargazers",
        access_token,
        per_page=per_page,
        page=page,
        accept_header="applicaiton/vnd.github.v3.star+json",
    )


# NOTE: unused, untested
# does not accept per page, exceeds if necessary
def get_repo_code_frequency(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """
    Returns code frequency for repository
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    :return: code frequency for repository
    """
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/code_frequency", access_token
    )


# NOTE: unused, untested
def get_repo_commit_activity(
    access_token: str, owner: str, repo: str
) -> Dict[str, Any]:
    """
    Returns commit activity for past year, broken by week
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    :return: commit activity for past year, broken by week
    """
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/commit_activity", access_token
    )


# NOTE: unused, untested
def get_repo_contributors(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """
    Returns contributors for a repository
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    :return: contributors for a repository
    """
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/contributors", access_token
    )


# NOTE: unused, untested
def get_repo_weekly_commits(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """
    Returns contributions by week, owner/non-owner
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    :return: contributions by week, owner/non-owner
    """
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/participation", access_token
    )


# NOTE: unused, untested
def get_repo_hourly_commits(access_token: str, owner: str, repo: str) -> Dict[str, Any]:
    """
    Returns contributions by day, hour for repository
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    """
    return get_template(
        BASE_URL + owner + "/" + repo + "/stats/punch_card", access_token
    )


def get_repo_commits(
    owner: str,
    repo: str,
    user: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    page: int = 1,
    access_token: Optional[str] = None,
) -> List[RawCommit]:
    """
    Returns most recent commits
    :param access_token: GitHub access token
    :param owner: repository owner
    :param repo: repository name
    :param user: optional GitHub user if not owner
    :param since: optional datetime to start from
    :param until: optional datetime to end at
    :param page: optional page number
    :return: Up to 100 commits from page
    """
    user = user if user is not None else owner
    query = BASE_URL + owner + "/" + repo + "/commits?author=" + user
    if since is not None:
        query += f"&since={str(since)}"
    if until is not None:
        query += f"&until={str(until)}"
    try:
        data = get_template_plural(query, access_token, page=page)

        def extract_info(x: Any) -> RawCommit:
            dt = x["commit"]["committer"]["date"]
            temp = {
                "timestamp": datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ"),
                "node_id": x["node_id"],
            }
            return RawCommit.model_validate(temp)

        return list(map(extract_info, data))
    except RESTError:
        return []
    except Exception as e:
        logging.exception(e)
        return []
