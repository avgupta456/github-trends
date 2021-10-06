# type: ignore

from typing import List, Tuple

from svgwrite import Drawing

from src.models.user.analytics import LanguageStats

from src.svg.template import get_template, get_bar_section, format_number


def get_top_langs_svg(
    data: List[LanguageStats], time_str: str, use_percent: bool = False
) -> Drawing:
    d, dp = get_template(
        width=300,
        height=285,
        padding=20,
        header_text="Most Used Languages",
        subheader_text=time_str,
        debug=False,
    )

    dataset: List[Tuple[str, str, List[Tuple[float, str]]]] = []
    for x in data[1:6]:
        if use_percent:
            dataset.append((x.lang, str(x.percent) + "%", [(x.percent, x.color)]))
        else:
            percent = 100 * x.changed / data[1].changed
            dataset.append((x.lang, format_number(x.changed), [(percent, x.color)]))

    section = get_bar_section(
        d=d, dataset=dataset, padding=45, bar_width=210 if use_percent else 195
    )

    dp.add(section)
    d.add(dp)
    return d
