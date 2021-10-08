# type: ignore

from typing import List, Tuple

from svgwrite import Drawing

from src.models.user.analytics import LanguageStats

from src.svg.template import (
    get_lang_name_section,
    get_template,
    get_bar_section,
    format_number,
)


def get_top_langs_svg(
    data: List[LanguageStats],
    time_str: str,
    use_percent: bool,
    loc_metric: str,
    commits_excluded: int,
    compact: bool,
) -> Drawing:
    subheader = time_str
    if not use_percent:
        subheader += " | " + ("LOC Changed" if loc_metric == "changed" else "LOC Added")
    if commits_excluded > 50:
        subheader += " | " + str(commits_excluded) + " commits excluded"

    d, dp = get_template(
        width=300,
        height=175 if compact else 285,
        padding=20,
        header_text="Most Used Languages",
        subheader_text=subheader,
        debug=False,
    )

    dataset: List[Tuple[str, str, List[Tuple[float, str]]]] = []
    padding, width = 0, 0
    if compact:
        data_row = []
        for x in data[1:6]:
            data_row.append((x.percent, x.color))
        dataset.append(("", "", data_row))
        padding, width = 30, 260
    else:
        for x in data[1:6]:
            if use_percent:
                dataset.append((x.lang, str(x.percent) + "%", [(x.percent, x.color)]))
            else:
                percent = 100 * x.loc / data[1].loc
                dataset.append((x.lang, format_number(x.loc), [(percent, x.color)]))
        padding, width = 45, 210 if use_percent else 195

    dp.add(get_bar_section(d=d, dataset=dataset, padding=padding, bar_width=width))

    langs = [(x.lang + " " + str(x.percent) + "%", x.color) for x in data[1:6]]
    if compact:
        dp.add(get_lang_name_section(d=d, data=langs))

    d.add(dp)
    return d
