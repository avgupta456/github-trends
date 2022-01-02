from collections import defaultdict
from json import load
from typing import Dict, List, Optional, Union

from src.constants import BLACKLIST, CUTOFF, DEFAULT_COLOR, FILE_CUTOFF
from src.data.github.graphql import RawCommit, RawRepo
from src.data.github.rest import RawCommitFile

EXTENSIONS: Dict[str, Dict[str, str]] = load(open("./src/data/github/extensions.json"))

t_langs = Dict[str, Dict[str, Union[int, str]]]


def get_commit_languages(
    commit: Optional[RawCommit],
    files: Optional[List[RawCommitFile]],
    repo: RawRepo,
) -> t_langs:
    out: t_langs = defaultdict(
        lambda: {"additions": 0, "deletions": 0, "color": DEFAULT_COLOR}
    )

    if commit is None:
        return {}

    if max(commit.additions, commit.deletions) == 0:
        return {}

    if max(commit.additions, commit.deletions) > 10 * CUTOFF:
        # assummed to be auto-generated or copied
        return {}

    pr_coverage = 0
    if len(commit.prs.nodes) > 0:
        pr_obj = commit.prs.nodes[0]
        pr_files = pr_obj.files.nodes
        total_changed = sum([x.additions + x.deletions for x in pr_files])
        pr_coverage = total_changed / max(1, (pr_obj.additions + pr_obj.deletions))

    if files is not None:
        for file in files:
            filename = file.filename.split(".")
            extension = "" if len(filename) <= 1 else filename[-1]
            lang = EXTENSIONS.get("." + extension, None)
            if (
                lang is not None
                and lang["name"] not in BLACKLIST
                and max(file.additions, file.deletions) > 0
                and max(file.additions, file.deletions) < FILE_CUTOFF
            ):
                out[lang["name"]]["color"] = lang["color"]
                out[lang["name"]]["additions"] += file.additions  # type: ignore
                out[lang["name"]]["deletions"] += file.deletions  # type: ignore
    elif len(commit.prs.nodes) > 0 and pr_coverage > 0.25:
        pr = commit.prs.nodes[0]
        total_additions, total_deletions = 0, 0
        for file in pr.files.nodes:
            filename = file.path.split(".")
            extension = "" if len(filename) <= 1 else filename[-1]
            lang = EXTENSIONS.get("." + extension, None)
            if (
                lang is not None
                and lang["name"] not in BLACKLIST
                and max(file.additions, file.deletions) > 0
                and max(file.additions, file.deletions) < FILE_CUTOFF
            ):
                out[lang["name"]]["color"] = lang["color"]
                out[lang["name"]]["additions"] += file.additions  # type: ignore
                out[lang["name"]]["deletions"] += file.deletions  # type: ignore
            total_additions += file.additions
            total_deletions += file.deletions
        for lang in out:
            raw_additions: int = out[lang]["additions"]  # type: ignore
            additions = round(
                min(pr.additions, commit.additions)
                * raw_additions
                / max(1, total_additions)
            )
            raw_deletions: int = out[lang]["deletions"]  # type: ignore
            deletions = round(
                min(pr.deletions, commit.deletions)
                * raw_deletions
                / max(1, total_deletions)
            )
            out[lang]["additions"] = additions
            out[lang]["deletions"] = deletions
    elif commit.additions + commit.deletions > CUTOFF:
        # assummed to be auto generated
        return {}
    else:
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

    return dict(out)
