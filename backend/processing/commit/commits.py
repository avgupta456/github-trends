from typing import Any, Dict

from external.github_api.rest.commit import get_commit

import json

with open("processing/commit/extensions.json") as f:
    extensions = json.load(f)


def get_commit_languages(
    owner: str, repo: str, commit_sha: str, cutoff: int = 1000
) -> Dict[str, Dict[str, int]]:
    files = get_commit(owner, repo, commit_sha)["files"]
    languages: Dict[str, Dict[str, Any]] = {}
    for file in files:
        try:
            language = extensions["." + file["filename"].split(".")[-1]]
            if language not in languages:
                languages[language] = {}
                languages[language]["additions"] = 0
                languages[language]["deletions"] = 0
                languages[language]["changes"] = 0
            if max(file["additons"], file["deletions"], file["changes"]) <= cutoff:
                languages[language]["additions"] += file["additions"]
                languages[language]["deletions"] += file["deletions"]
                languages[language]["changes"] += file["changes"]
        except Exception as e:
            print(e)
    return languages
