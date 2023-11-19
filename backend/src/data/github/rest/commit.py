from typing import List, Optional

from src.data.github.rest.models import RawCommitFile
from src.data.github.rest.template import get_template

BASE_URL = "https://api.github.com/repos/"


def get_commit_files(
    owner: str, repo: str, sha: str, access_token: Optional[str] = None
) -> Optional[List[RawCommitFile]]:
    """
    Returns raw repository data
    :param owner: repository owner
    :param repo: repository name
    :param sha: commit sha
    :param access_token: GitHub access token
    :return: repository data
    """

    try:
        output = get_template(
            BASE_URL + owner + "/" + repo + "/commits/" + sha, access_token
        )
        files = output["files"]
        return [RawCommitFile.model_validate(f) for f in files]
    except Exception:
        return None
