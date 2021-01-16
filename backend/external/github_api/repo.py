import requests

from typing import Optional

s = requests.session()

BASE_URL = "https://api.github.com/repos/"


def get_repo(owner: str, repo: str) -> dict:
    """Returns raw repository data"""
    r = s.get(BASE_URL + owner + "/" + repo)
    return r.json()


def get_repo_languages(owner: str, repo: str) -> dict:
    """Returns repository language breakdown"""
    r = s.get(BASE_URL + owner + "/" + repo + "/languages")
    return r.json()


def get_repo_stargazers(owner: str, repo: str, per_page: Optional[int] = 100) -> dict:
    """Returns stargazers with timestamp for repository"""
    headers = {"Accept": "application/vnd.github.v3.star+json"}
    r = s.get(
        BASE_URL + owner + "/" + repo + "/stargazers?per_page=" + str(per_page),
        headers=headers,
    )
    print(r.headers)
    return r.json()
