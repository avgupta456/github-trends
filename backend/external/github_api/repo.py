from typing import Optional

from external.github_api.template import get_template

BASE_URL = "https://api.github.com/repos/"


def get_repo(owner: str, repo: str) -> dict:
    """Returns raw repository data"""
    return get_template(BASE_URL + owner + "/" + repo)


def get_repo_languages(owner: str, repo: str) -> dict:
    """Returns repository language breakdown"""
    return get_template(BASE_URL + owner + "/" + repo + "/languages", plural=True)


def get_repo_stargazers(owner: str, repo: str, per_page: Optional[int] = 100) -> dict:
    """Returns stargazers with timestamp for repository"""
    return get_template(
        BASE_URL + owner + "/" + repo + "/stargazers",
        plural=True,
        per_page=per_page,
        accept_header="applicaiton/vnd.github.v3.star+json",
    )

