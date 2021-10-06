# type: ignore

from typing import List

from svgwrite import Drawing
from svgwrite.container import Group

from src.models.user.analytics import LanguageStats

from src.svg.style import style


def format_number(num: int) -> str:
    if num > 10000:
        return "~" + str(int(num / 1000)) + "k lines"
    elif num > 1000:
        return "~" + str(int(num / 100) / 10) + "k lines"
    elif num > 100:
        return "~" + str(int(num / 100) * 100) + " lines"
    else:
        return "<100 lines"


def get_top_langs_svg(
    data: List[LanguageStats], time_str: str, use_percent: bool = True
) -> Drawing:
    d = Drawing(size=(300, 285))
    d.defs.add(d.style(style))

    d.add(
        d.rect(
            size=(299, 284),
            insert=(0.5, 0.5),
            rx=4.5,
            stroke="#e4e2e2",
            fill="#fffefe",
        )
    )

    d.add(d.text("Most Used Languages", insert=(25, 35), class_="header"))
    d.add(d.text(time_str, insert=(25, 55), class_="subheader"))

    langs = Group(transform="translate(25, 75)")

    data_langs = data[1:]  # exclude "Total"
    for i in range(min(5, len(data_langs))):
        translate = "translate(0, " + str(40 * i) + ")"
        percent = (
            data_langs[i].percent
            if use_percent
            else 100 * data_langs[i].changed / data_langs[0].changed
        )
        color = data_langs[i].color or "#ededed"
        lang = Group(transform=translate)
        lang.add(d.text(data_langs[i].lang, insert=(2, 15), class_="lang-name"))
        if use_percent:
            lang.add(d.text(str(percent) + "%", insert=(215, 33), class_="lang-name"))
        else:
            lang.add(
                d.text(
                    format_number(data_langs[i].changed),
                    insert=(215, 33),
                    class_="lang-name",
                )
            )
        progress = Drawing(width="205", x="0", y="25")
        progress.add(d.rect(size=(205, 8), insert=(0, 0), rx=5, ry=5, fill="#ddd"))
        progress.add(
            d.rect(
                size=(2.05 * percent, 8),
                insert=(0, 0),
                rx=5,
                ry=5,
                fill=color,
            )
        )
        lang.add(progress)
        langs.add(lang)
    d.add(langs)

    return d
