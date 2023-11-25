# type: ignore

from collections import defaultdict
from typing import List, Tuple

from svgwrite import Drawing

from src.models.svg import RepoStats
from src.render.error import get_no_data_svg
from src.render.template import get_bar_section, get_lang_name_section, get_template
from src.utils import format_number


def get_top_repos_svg(
    data: List[RepoStats],
    time_str: str,
    loc_metric: str,
    complete: bool,
    commits_excluded: int,
    use_animation: bool,
    theme: str,
) -> Drawing:
    header = "Most Contributed Repositories"
    subheader = time_str
    subheader += " | " + ("LOC Changed" if loc_metric == "changed" else "LOC Added")
    if not complete:
        subheader += " | Incomplete (refresh to update)"
    elif commits_excluded > 50:
        subheader += f" | {commits_excluded} commits excluded"

    if len(data) == 0:
        return get_no_data_svg(header, subheader)

    d, dp = get_template(
        width=300,
        height=285,
        padding=20,
        header_text=header,
        subheader_text=subheader,
        use_animation=use_animation,
        debug=False,
        theme=theme,
    )

    dataset: List[Tuple[str, str, List[Tuple[float, str]]]] = []
    total = max(x.loc for x in data)
    for x in data[:4]:
        data_row = [
            (100 * lang.loc / total, lang.color)
            for lang in sorted(x.langs, key=lambda x: x.loc, reverse=True)
        ]

        name = "private/repository" if x.private else x.repo
        dataset.append((name, format_number(x.loc), data_row))

    dp.add(
        get_bar_section(d=d, dataset=dataset, theme=theme, padding=45, bar_width=195)
    )

    langs = defaultdict(int)
    for x in data[:4]:
        for lang in x.langs:
            langs[(lang.lang, lang.color)] += lang.loc
    langs = sorted(langs.items(), key=lambda x: x[1], reverse=True)
    langs = [lang[0] for lang in langs[:6]]

    columns = {1: 1, 2: 2, 3: 3, 4: 2, 5: 3, 6: 3}[len(langs)]
    padding = 215 + (10 if columns == len(langs) else 0)
    dp.add(
        get_lang_name_section(
            d=d, data=langs, theme=theme, columns=columns, padding=padding
        )
    )

    d.add(dp)
    return d
