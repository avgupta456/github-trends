from typing import Any, Dict

from svgwrite import Drawing  # type: ignore

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

    d.add(d.text("Most Used Languages", insert=(25, 35), class_="header"))  # type: ignore

    return d
