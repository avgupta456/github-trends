from typing import Any, Dict, List

from external.github_api.graphql.commit import get_commits


def get_commits_languages(
    node_ids: List[str], cutoff: int = 1000
) -> List[Dict[str, Dict[str, int]]]:
    out: List[Dict[str, Dict[str, int]]] = []
    all_data: List[Dict[str, Any]] = []
    for i in range(0, len(node_ids), 100):
        # suppress pylance error
        data: List[Dict[str, Any]] = get_commits(
            node_ids[i : min(len(node_ids), i + 100)]
        )[
            "data"
        ][  # type: ignore
            "nodes"
        ]  # type: ignore
        all_data.extend(data)

    for commit in all_data:
        out.append({})
        if commit["additions"] + commit["deletions"] < cutoff:
            languages = commit["repository"]["languages"]["edges"]
            num_langs = min(len(languages), commit["changedFiles"])
            total_repo_size = sum(
                [language["size"] for language in languages[:num_langs]]
            )
            for language in languages[:num_langs]:
                lang_name = language["node"]["name"]
                out[-1][lang_name] = {}  # type: ignore
                out[-1][lang_name]["additions"] = round(
                    commit["additions"] * language["size"] / total_repo_size
                )
                out[-1][lang_name]["deletions"] = round(
                    commit["deletions"] * language["size"] / total_repo_size
                )

    return out
