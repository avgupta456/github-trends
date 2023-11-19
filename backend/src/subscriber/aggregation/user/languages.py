from json import load
from typing import Any, Dict, List, Optional, Union

from src.constants import BLACKLIST, CUTOFF, DEFAULT_COLOR, FILE_CUTOFF
from src.data.github.graphql import RawCommit, RawRepo
from src.data.github.rest import RawCommitFile

EXTENSIONS: Dict[str, Dict[str, str]] = load(open("./src/data/github/extensions.json"))


class CommitLanguages:
    def __init__(self):
        self.langs: Dict[str, Dict[str, Union[str, int]]] = {}

    def __repr__(self):
        return str(self.langs)

    def add_lines(
        self, name: str, color: Optional[str], additions: int, deletions: int
    ):
        if (
            name not in BLACKLIST
            and max(additions, deletions) > 0
            and max(additions, deletions) < FILE_CUTOFF
        ):
            color = color or DEFAULT_COLOR
            if name not in self.langs:
                self.langs[name] = {"color": color, "additions": 0, "deletions": 0}
            self.langs[name]["additions"] += additions  # type: ignore
            self.langs[name]["deletions"] += deletions  # type: ignore

    def normalize(self, add_ratio: float, del_ratio: float):
        for lang in self.langs:
            new_add = round(int(self.langs[lang]["additions"]) * add_ratio)
            self.langs[lang]["additions"] = new_add
            new_del = round(int(self.langs[lang]["deletions"]) * del_ratio)
            self.langs[lang]["deletions"] = new_del

    def __add__(self, other: "CommitLanguages"):
        for lang in other.langs:
            if lang not in self.langs:
                self.langs[lang] = other.langs[lang].copy()
            else:
                self.langs[lang]["additions"] += other.langs[lang]["additions"]  # type: ignore
                self.langs[lang]["deletions"] += other.langs[lang]["deletions"]  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return self.langs


def get_commit_languages(
    commit: Optional[RawCommit],
    files: Optional[List[RawCommitFile]],
    repo: RawRepo,
) -> CommitLanguages:
    out = CommitLanguages()

    if commit is None:
        return out

    if max(commit.additions, commit.deletions) == 0:
        return out

    # assummed to be auto-generated or copied
    if max(commit.additions, commit.deletions) > 10 * CUTOFF or (
        max(commit.additions, commit.deletions) > CUTOFF
        and min(commit.additions, commit.deletions) == 0
    ):
        return out

    pr_coverage = 0
    if len(commit.prs.nodes) > 0:
        pr_obj = commit.prs.nodes[0]
        pr_files = pr_obj.files.nodes
        total_changed = sum(x.additions + x.deletions for x in pr_files)
        pr_coverage = total_changed / max(1, (pr_obj.additions + pr_obj.deletions))

    if files is not None:
        for file in files:
            filename = file.filename.split(".")
            extension = "" if len(filename) <= 1 else filename[-1]
            lang = EXTENSIONS.get(f".{extension}", None)
            if lang is not None:
                out.add_lines(
                    lang["name"], lang["color"], file.additions, file.deletions
                )
    elif len(commit.prs.nodes) > 0 and pr_coverage > 0.25:
        pr = commit.prs.nodes[0]
        total_additions, total_deletions = 0, 0
        for file in pr.files.nodes:
            filename = file.path.split(".")
            extension = "" if len(filename) <= 1 else filename[-1]
            lang = EXTENSIONS.get(f".{extension}", None)
            if lang is not None:
                out.add_lines(
                    lang["name"], lang["color"], file.additions, file.deletions
                )
            total_additions += file.additions
            total_deletions += file.deletions
        add_ratio = min(pr.additions, commit.additions) / max(1, total_additions)
        del_ratio = min(pr.deletions, commit.deletions) / max(1, total_deletions)
        out.normalize(add_ratio, del_ratio)
    elif commit.additions + commit.deletions > 2 * CUTOFF:
        # assummed to be auto generated
        return out
    else:
        repo_info = repo.languages.edges
        languages = [x for x in repo_info if x.node.name not in BLACKLIST]
        total_repo_size = sum(language.size for language in languages)
        for language in languages:
            lang_name = language.node.name
            lang_color = language.node.color
            lang_size = language.size
            additions = round(commit.additions * lang_size / total_repo_size)
            deletions = round(commit.deletions * lang_size / total_repo_size)
            out.add_lines(lang_name, lang_color, additions, deletions)

    return out
