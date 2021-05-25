from typing import Any, Dict

from external.github_api.rest.template import get_template

BASE_URL = "https://api.github.com/repos/"


def get_commit(owner: str, repo: str, commit_sha: str) -> Dict[str, Any]:
    """Returns raw commit data"""
    return get_template(BASE_URL + owner + "/" + repo + "/commits/" + commit_sha)
