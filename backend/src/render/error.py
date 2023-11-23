# type: ignore

from svgwrite import Drawing

from src.constants import BACKEND_URL
from src.render.style import styles_no_animation, themes
from src.render.template import get_template

THEME = "classic"


def get_error_svg() -> Drawing:
    d = Drawing(size=(300, 285))
    d.defs.add(d.style(styles_no_animation[THEME]))

    d.add(
        d.rect(
            size=(299, 284),
            insert=(0.5, 0.5),
            rx=4.5,
            stroke=themes[THEME]["border_color"],
            fill=themes[THEME]["bg_color"],
        )
    )

    d.add(d.text("Unknown Error", insert=(25, 35), class_=f"{THEME}-header"))

    d.add(
        d.text(
            "Please try again later or raise a ticket on GitHub",
            insert=(25, 60),
            class_=f"{THEME}-lang-name",
        )
    )

    d.add(
        d.image(f"{BACKEND_URL}/assets/error", insert=(85, 100), style="opacity: 50%")
    )

    return d


def get_empty_demo_svg(header: str) -> Drawing:
    d = Drawing(size=(300, 285))
    d.defs.add(d.style(styles_no_animation[THEME]))

    d.add(
        d.rect(
            size=(299, 284),
            insert=(0.5, 0.5),
            rx=4.5,
            stroke=themes[THEME]["border_color"],
            fill=themes[THEME]["bg_color"],
        )
    )

    d.add(d.text(header, insert=(25, 35), class_=f"{THEME}-header"))

    d.add(
        d.text(
            "Enter your username to start!",
            insert=(25, 60),
            class_=f"{THEME}-lang-name",
        )
    )

    d.add(
        d.image(
            f"{BACKEND_URL}/assets/stopwatch", insert=(85, 100), style="opacity: 50%"
        )
    )

    return d


def get_loading_svg() -> Drawing:
    d = Drawing(size=(300, 285))
    d.defs.add(d.style(styles_no_animation[THEME]))

    d.add(
        d.rect(
            size=(299, 284),
            insert=(0.5, 0.5),
            rx=4.5,
            stroke=themes[THEME]["border_color"],
            fill=themes[THEME]["bg_color"],
        )
    )

    d.add(
        d.text("Loading data, hang tight!", insert=(25, 35), class_=f"{THEME}-header")
    )

    d.add(
        d.text(
            "Please wait a couple seconds and refresh the page.",
            insert=(25, 60),
            class_=f"{THEME}-lang-name",
        )
    )

    d.add(
        d.image(
            f"{BACKEND_URL}/assets/stopwatch", insert=(85, 100), style="opacity: 50%"
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
        theme=THEME,
    )

    d.add(d.image(f"{BACKEND_URL}/assets/error", insert=(85, 80), style="opacity: 50%"))

    dp.add(d.text("No data to show", insert=(55, 220), class_=f"{THEME}-image-text"))

    d.add(dp)
    return d
