# type: ignore

from typing import List, Tuple

from svgwrite import Drawing

from src.models.user.analytics import RepoStats

from src.svg.template import get_template, get_bar_section, format_number


def get_top_repos_svg(
    data: List[RepoStats], time_str: str, commits_excluded: int
) -> Drawing:
    subheader = time_str
    if commits_excluded > 50:
        subheader += " | " + str(commits_excluded) + " commits excluded"

    d, dp = get_template(
        width=300,
        height=285,
        padding=20,
        header_text="Most Contributed Repositories",
        subheader_text=subheader,
        debug=False,
    )

    dataset: List[Tuple[str, str, List[Tuple[float, str]]]] = []
    total = data[0].changed
    for x in data[:5]:
        data_row = []
        for j, lang in enumerate(x.langs):
            data_row.append(
                (100 * (lang.additions + lang.deletions) / total, lang.color)
            )
        name = "Private Repository" if x.private else x.repo
        dataset.append((name, format_number(x.changed), data_row))

    section = get_bar_section(d=d, dataset=dataset, padding=45, bar_width=195)

    dp.add(section)
    d.add(dp)
    return d
