from typing import Optional, Dict, Any

from external.github_api.rest.template import get_template

BASE_URL = "https://api.github.com/repos/"


def get_repo(owner: str, repo: str) -> Dict[str, Any]:
    """Returns raw repository data"""
    return get_template(BASE_URL + owner + "/" + repo)


def get_repo_languages(owner: str, repo: str) -> Dict[str, Any]:
    """Returns repository language breakdown"""
    return get_template(BASE_URL + owner + "/" + repo + "/languages", plural=True)


def get_repo_stargazers(
    owner: str, repo: str, per_page: Optional[int] = 100
) -> Dict[str, Any]:
    """Returns stargazers with timestamp for repository"""
    return get_template(
        BASE_URL + owner + "/" + repo + "/stargazers",
        plural=True,
        per_page=per_page,
        accept_header="applicaiton/vnd.github.v3.star+json",
    )


# does not accept per page, exceeds if necessary
def get_repo_code_frequency(owner: str, repo: str) -> Dict[str, Any]:
    """Returns code frequency for repository"""
    return get_template(BASE_URL + owner + "/" + repo + "/stats/code_frequency")


def get_repo_commit_activity(owner: str, repo: str) -> Dict[str, Any]:
    """Returns commit activity for past year, broken by week"""
    return get_template(BASE_URL + owner + "/" + repo + "/stats/commit_activity")


def get_repo_contributors(owner: str, repo: str) -> Dict[str, Any]:
    """Returns contributors for a repository"""
    return get_template(BASE_URL + owner + "/" + repo + "/stats/contributors")


def get_repo_weekly_commits(owner: str, repo: str) -> Dict[str, Any]:
    """Returns contributions by week, owner/non-owner"""
    return get_template(BASE_URL + owner + "/" + repo + "/stats/participation")


def get_repo_hourly_commits(owner: str, repo: str) -> Dict[str, Any]:
    """Returns contributions by day, hour for repository"""
    return get_template(BASE_URL + owner + "/" + repo + "/stats/punch_card")
