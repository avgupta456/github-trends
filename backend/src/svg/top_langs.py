# type: ignore

from typing import Any, Dict

from svgwrite import Drawing
from svgwrite.container import Group

from src.svg.style import style


def get_top_langs_svg(data: Dict[str, Any]) -> Drawing:
    d = Drawing(size=(300, 285))
    d.defs.add(d.style(style))  # type: ignore

    d.add(  # type: ignore
        d.rect(  # type: ignore
            size=(299, 284),
            insert=(0.5, 0.5),
            rx=4.5,
            stroke="#e4e2e2",
            fill="#fffefe",
        )
    )

    d.add(d.text("Most Used Languages", insert=(25, 35), class_="header"))

    langs = Group(transform="translate(25, 55)")

    data_langs = data["top_languages"][1:]
    for i in range(min(5, len(data_langs))):
        translate = "translate(0, " + str(40 * i) + ")"
        percent = data_langs[i]["percent"]
        lang1 = Group(transform=translate)
        lang1.add(d.text(data_langs[i]["lang"], insert=(2, 15), class_="lang-name"))
        lang1.add(d.text(str(percent) + "%", insert=(215, 33), class_="lang-name"))
        progress = Drawing(width="205", x="0", y="25")
        progress.add(d.rect(size=(205, 8), insert=(0, 0), rx=5, ry=5, fill="#ddd"))
        progress.add(
            d.rect(size=(2.05 * percent, 8), insert=(0, 0), rx=5, ry=5, fill="#DA5B0B")
        )
        lang1.add(progress)
        langs.add(lang1)
    d.add(langs)

    return d
