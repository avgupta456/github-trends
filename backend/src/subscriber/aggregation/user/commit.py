from collections import defaultdict
from json import load
from typing import Dict, List, Optional, Union

from src.constants import BLACKLIST, CUTOFF, DEFAULT_COLOR
from src.data.github.graphql import RawCommit, RawRepo
from src.data.github.rest import RawCommitFile

EXTENSIONS: Dict[str, Dict[str, str]] = load(open("./src/data/github/extensions.json"))

t_langs = Dict[str, Dict[str, Union[int, str]]]


def get_commit_languages(
    commit: Optional[RawCommit],
    files: Optional[List[RawCommitFile]],
    repo: RawRepo,
) -> t_langs:
    print(commit)
    print(files)

    out: t_langs = defaultdict(
        lambda: {"additions": 0, "deletions": 0, "color": DEFAULT_COLOR}
    )

    if commit is None:
        return {}

    if max(commit.additions, commit.deletions) == 0:
        return {}

    if commit.additions + commit.deletions > CUTOFF:
        # assummed to be auto generated
        return {}

    if files is not None:
        for file in files:
            filename = file.filename.split(".")
            extension = "" if len(filename) <= 1 else filename[-1]
            lang = EXTENSIONS.get("." + extension, None)
            if (
                lang is not None
                and lang not in BLACKLIST
                and max(file.additions, file.deletions) > 0
            ):
                out[lang["name"]]["color"] = lang["color"]
                out[lang["name"]]["additions"] += file.additions  # type: ignore
                out[lang["name"]]["deletions"] += file.deletions  # type: ignore
    elif commit is not None and len(commit.prs.nodes) > 0:
        pr = commit.prs.nodes[0]
        total_additions, total_deletions = 0, 0
        for file in pr.files.nodes:
            filename = file.path.split(".")
            extension = "" if len(filename) <= 1 else filename[-1]
            lang = EXTENSIONS.get("." + extension, None)
            if (
                lang is not None
                and lang not in BLACKLIST
                and max(file.additions, file.deletions) > 0
            ):
                out[lang["name"]]["color"] = lang["color"]
                out[lang["name"]]["additions"] += file.additions  # type: ignore
                out[lang["name"]]["deletions"] += file.deletions  # type: ignore
            total_additions += file.additions
            total_deletions += file.deletions
        for lang in out:
            out[lang]["additions"] = round(
                commit.additions * out[lang]["additions"] / max(1, total_additions)
            )
            out[lang]["deletions"] = round(
                commit.deletions * out[lang]["deletions"] / max(1, total_deletions)
            )
    elif commit is not None:
        repo_info = repo.languages.edges
        languages = [x for x in repo_info if x.node.name not in BLACKLIST]
        total_repo_size = sum([language.size for language in languages])
        for language in languages:
            lang_name = language.node.name
            lang_color = language.node.color
            lang_size = language.size
            additions = round(commit.additions * lang_size / total_repo_size)
            deletions = round(commit.deletions * lang_size / total_repo_size)
            if additions > 0 or deletions > 0:
                out[lang_name] = {
                    "additions": additions,
                    "deletions": deletions,
                    "color": lang_color or DEFAULT_COLOR,
                }

    out = dict(out)
    print(out)
    print()

    return out


"""
def get_commits_languages(
    node_ids: List[str],
    commit_repos: List[str],
    repo_infos: Dict[str, RawRepo],
    cutoff: int = CUTOFF,
    cutoff_per_file: int = CUTOFF_PER_FILE,
    max_cutoff: int = MAX_CUTOFF,
    access_token: Optional[str] = None,
):
    all_data = get_commits(node_ids, access_token)

    out: List[Dict[str, Dict[str, Union[int, str]]]] = []
    for commit, commit_repo in zip(all_data, commit_repos):
        out.append({})
        if commit is None:
            continue

        changed = commit.additions + commit.deletions
        per_file = changed / max(1, commit.changed_files)
        if (changed < cutoff or per_file < cutoff_per_file) and (changed < max_cutoff):
            repo_info = repo_infos[commit_repo].languages.edges
            languages = [x for x in repo_info if x.node.name not in BLACKLIST]
            total_repo_size = sum([language.size for language in languages])
            for language in languages:
                lang_name = language.node.name
                lang_color = language.node.color
                lang_size = language.size
                additions = round(commit.additions * lang_size / total_repo_size)
                deletions = round(commit.deletions * lang_size / total_repo_size)
                if additions > 0 or deletions > 0:
                    out[-1][lang_name] = {
                        "additions": additions,
                        "deletions": deletions,
                        "color": lang_color or DEFAULT_COLOR,
                    }

    return all_data
"""
