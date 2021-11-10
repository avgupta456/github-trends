# type: ignore

from typing import List, Tuple

from svgwrite import Drawing

from src.publisher.aggregation.user.models import RepoStats
from src.publisher.render.error import get_no_data_svg
from src.publisher.render.template import (
    format_number,
    get_bar_section,
    get_lang_name_section,
    get_template,
)


def get_top_repos_svg(
    data: List[RepoStats],
    time_str: str,
    loc_metric: str,
    commits_excluded: int,
    use_animation: bool,
) -> Drawing:
    header = "Most Contributed Repositories"
    subheader = time_str
    subheader += " | " + ("LOC Changed" if loc_metric == "changed" else "LOC Added")
    if commits_excluded > 50:
        subheader += " | " + str(commits_excluded) + " commits excluded"

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
    )

    dataset: List[Tuple[str, str, List[Tuple[float, str]]]] = []
    total = data[0].loc
    for x in data[:4]:
        data_row = []
        for lang in x.langs:
            data_row.append((100 * lang.loc / total, lang.color))
        name = "private/repository" if x.private else x.repo
        dataset.append((name, format_number(x.loc), data_row))

    dp.add(get_bar_section(d=d, dataset=dataset, padding=45, bar_width=195))

    langs = {}
    for x in data[:4]:
        for lang in x.langs:
            langs[lang.lang] = lang.color
    langs = list(langs.items())[:6]

    columns = {1: 1, 2: 2, 3: 3, 4: 2, 5: 3, 6: 3}[len(langs)]
    padding = 215 + (10 if columns == len(langs) else 0)
    dp.add(get_lang_name_section(d=d, data=langs, columns=columns, padding=padding))

    d.add(dp)
    return d
