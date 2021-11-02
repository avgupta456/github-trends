# type: ignore

from svgwrite import Drawing
from src.constants import BACKEND_URL

from src.publisher.render.style import style
from src.publisher.render.template import get_template


def get_error_svg() -> Drawing:
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


def get_loading_svg() -> Drawing:
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

    d.add(d.text("Loading data, hang tight!", insert=(25, 35), class_="header"))

    d.add(
        d.text(
            "Please wait a couple seconds and refresh the page.",
            insert=(25, 60),
            class_="lang-name",
        )
    )

    d.add(
        d.image(
            BACKEND_URL + "/assets/stopwatch", insert=(85, 100), style="opacity: 50%"
        )
    )

    return d


def get_no_data_svg(header: str, subheader: str) -> Drawing:
    d, dp = get_template(
        width=300,
        height=285,
        padding=20,
        header_text=header,
        subheader_text=subheader,
        debug=False,
    )

    d.add(d.image(BACKEND_URL + "/assets/error", insert=(85, 80), style="opacity: 50%"))
    dp.add(d.text("No data to show", insert=(55, 220), class_="no-data"))

    d.add(dp)
    return d


def get_empty_demo_svg(header: str) -> Drawing:
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

    d.add(d.text(header, insert=(25, 35), class_="header"))

    d.add(
        d.text(
            "Enter your username to start!",
            insert=(25, 60),
            class_="lang-name",
        )
    )

    d.add(
        d.image(
            BACKEND_URL + "/assets/stopwatch", insert=(85, 100), style="opacity: 50%"
        )
    )

    return d
