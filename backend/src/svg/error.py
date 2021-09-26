# type: ignore

from svgwrite import Drawing
from src.constants import BACKEND_URL

from src.svg.style import style


def get_error_svg() -> Drawing:
    d = Drawing(viewBox=("0 0 300 285"), class_="svg")
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

    d.add(d.text("Unknown Error", insert=(25, 35), class_="header"))

    d.add(
        d.text(
            "Please try again later or raise a ticket on GitHub",
            insert=(25, 60),
            class_="lang-name",
        )
    )

    d.add(
        d.image(BACKEND_URL + "/assets/error", insert=(85, 100), style="opacity: 50%")
    )

    return d
