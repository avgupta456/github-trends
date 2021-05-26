from typing import Any, Dict, List

from external.github_api.graphql.commit import get_commits


blacklist = ["Jupyter Notebook"]


def get_commits_languages(
    node_ids: List[str], cutoff: int = 1000
) -> List[Dict[str, Dict[str, int]]]:
    out: List[Dict[str, Dict[str, int]]] = []
    all_data: List[Dict[str, Any]] = []
    for i in range(0, len(node_ids), 100):
        # TODO: handle exception to get_commits
        # ideally would alert users somehow that data is incomplete
        try:
            raw_data = get_commits(node_ids[i : min(len(node_ids), i + 100)])
            data: List[Dict[str, Any]] = raw_data["data"]["nodes"]  # type: ignore
            all_data.extend(data)
        except Exception:
            print("Commit Exception")

    for commit in all_data:
        out.append({})
        if commit["additions"] + commit["deletions"] < cutoff:
            languages = [
                x
                for x in commit["repository"]["languages"]["edges"]
                if x["node"]["name"] not in blacklist
            ]
            num_langs = min(len(languages), commit["changedFiles"])
            total_repo_size = sum(
                [language["size"] for language in languages[:num_langs]]
            )
            for language in languages[:num_langs]:
                lang_name = language["node"]["name"]
                additions = round(
                    commit["additions"] * language["size"] / total_repo_size
                )
                deletions = round(
                    commit["deletions"] * language["size"] / total_repo_size
                )
                if additions > 0 or deletions > 0:
                    out[-1][lang_name] = {
                        "additions": additions,
                        "deletions": deletions,
                    }

    return out
