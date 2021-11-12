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
        "bar_color": "#333333",
    },
    "bright_lights": {
        "header_color": "#fff",
        "subheader_color": "#0E86D4",
        "text_color": "#B1D4E0",
        "bg_color": "#003060",
        "border_color": "#0E86D4",
        "bar_color": "#68BBE3",
    },
    "rosettes": {
        "header_color": "#fff",
        "subheader_color": "#B6E2D3",
        "text_color": "#FAE8E0",
        "bg_color": "#EF7C8E",
        "border_color": "#B6E2D3",
        "bar_color": "#D8A7B1",
    },
    "ferns": {
        "header_color": "#116530",
        "subheader_color": "#18A558",
        "text_color": "#116530",
        "bg_color": "#A3EBB1",
        "border_color": "#21B6A8",
        "bar_color": "#21B6A8",
    },
    "synthwaves": {
        "header_color": "#e2e9ec",
        "subheader_color": "#e5289e",
        "text_color": "#ef8539",
        "bg_color": "#2b213a",
        "border_color": "#e5289e",
        "bar_color": "#e5289e",
    }
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
            rule[0].replace(".", "." + theme + "-")
            + " {"
            + "\n".join(item[0] for item in rule[1] if (use_animation or not item[1]))
            + "}"
            for rule in _style
            if use_animation or not rule[2]
        ]
    )


styles = {k: get_style(k) for k in themes.keys()}
styles_no_animation = {k: get_style(k, False) for k in themes.keys()}
