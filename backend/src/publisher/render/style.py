from typing import List, Tuple

themes = {
    "classic": {
        "header_color": "#2f80ed",
        "subheader_color": "#666",
        "text_color": "#333",
        "bg_color": "#fffefe",
        "border_color": "#e4e2e2",
        "bar_color": "#ddd",
    },
    "dark": {
        "header_color": "#fff",
        "subheader_color": "#9f9f9f",
        "text_color": "#9f9f9f",
        "bg_color": "#151515",
        "border_color": "#e4e2e2",
        "bar_color": "#333",
    },
    "bright_lights": {
        "header_color": "#fff",
        "subheader_color": "#0e86d4",
        "text_color": "#b1d4e0",
        "bg_color": "#003060",
        "border_color": "#0e86d4",
        "bar_color": "#ddd",
    },
    "rosettes": {
        "header_color": "#fff",
        "subheader_color": "#b6e2d3",
        "text_color": "#fae8e0",
        "bg_color": "#ef7c8e",
        "border_color": "#b6e2d3",
        "bar_color": "#ddd",
    },
    "ferns": {
        "header_color": "#116530",
        "subheader_color": "#18a558",
        "text_color": "#116530",
        "bg_color": "#a3ebb1",
        "border_color": "#21b6a8",
        "bar_color": "#ddd",
    },
    "synthwaves": {
        "header_color": "#e2e9ec",
        "subheader_color": "#e5289e",
        "text_color": "#ef8539",
        "bg_color": "#2b213a",
        "border_color": "#e5289e",
        "bar_color": "#ddd",
    },
}


def get_style(theme: str = "classic", use_animation: bool = True) -> str:
    # List[Tuple["selector", List[Tuple["property", "is_animation"]], "is_animation"]]
    _style: List[Tuple[str, List[Tuple[str, bool]], bool]] = [
        (
            ".header",
            [
                ("font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;", False),
                ("fill: " + themes[theme]["header_color"] + ";", False),
                ("animation: fadeInAnimation 0.8s ease-in-out forwards;", True),
            ],
            False,
        ),
        (
            ".subheader",
            [
                ("font: 500 10px 'Segoe UI', Ubuntu, Sans-Serif;", False),
                ("fill: " + themes[theme]["subheader_color"] + ";", False),
                ("animation: fadeInAnimation 0.8s ease-in-out forwards;", True),
            ],
            False,
        ),
        (
            ".lang-name",
            [
                ("font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif;", False),
                ("fill: " + themes[theme]["text_color"] + ";", False),
            ],
            False,
        ),
        (
            ".image-text",
            [
                ("font: 500 20px 'Segoe UI', Ubuntu, Sans-Serif;", False),
                ("fill: " + themes[theme]["text_color"] + ";", False),
                ("opacity: 50%;", False),
            ],
            False,
        ),
        (
            "@keyframes fadeInAnimation",
            [("from { opacity: 0; } to { opacity: 1; }", True)],
            True,
        ),
    ]

    return "\n".join(
        [
            (
                (rule[0].replace(".", f".{theme}-") + " {")
                + "\n".join(
                    item[0] for item in rule[1] if (use_animation or not item[1])
                )
                + "}"
            )
            for rule in _style
            if use_animation or not rule[2]
        ]
    )


styles = {k: get_style(k) for k in themes.keys()}
styles_no_animation = {k: get_style(k, False) for k in themes.keys()}
