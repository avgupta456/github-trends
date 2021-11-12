from typing import List, Tuple, Dict, Any

# List[Tuple["selector", List[Tuple["property", "is_animation"]], "is_animation"]]

background_styles: Dict[str, Dict[str, str]] = {
    "classic": {
        "main_fill_color": "#e4e2e2",
        "sub_fill_color": "#fff",
        "border_color": "#fffefe",
        "bar_default_color": "#ddd",
    },
    "dark": {
        "main_fill_color": "#1a1a1a",
        "sub_fill_color": "#1f1f1f",
        "border_color": "#7B8794",
        "bar_default_color": "#333333",
    }, 
    "error": {
        "main_fill_color": "#fffefe",
        "border_color": "#e4e2e2",
    }
}

general_styles: Dict[str, Dict[str, str]] = {
    "classic": {
        "header_text_color": "#2f80ed",
        "subheader_text_color": "#666",
        "langname_color": "#333",
        "no_data_color": "#777",
    },
    "dark": {
        "header_text_color": "#2f80ed",
        "subheader_text_color": "#ebebeb",
        "langname_color": "#f5f5f5",
        "no_data_color": "#c9c9c9",
    },
    "error": {
        "header_text_color": "#2f80ed",
        "subheader_text_color": "#666",
        "langname_color": "#333",
        "no_data_color": "#777",
    }
}

def get_theme_style(theme: str) -> Tuple[Any, Any]:
    _style: List[Tuple[str, List[Tuple[str, bool]], bool]] = [
        (
            ".header",
            [
                ("font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;", False),
                ("fill: " + general_styles[theme]["header_text_color"] + ";", False),
                ("animation: fadeInAnimation 0.8s ease-in-out forwards;", True),
            ],
            False,
        ),
        (
            ".subheader",
            [
                ("font: 500 10px 'Segoe UI', Ubuntu, San-Serif;", False),
                ("fill: " + general_styles[theme]["subheader_text_color"] + ";", False),
                ("animation: fadeInAnimation 0.8s ease-in-out forwards;", True),
            ],
            False,
        ),
        (
            ".lang-name",
            [
                ("font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif;", False),
                ("fill: " + general_styles[theme]["langname_color"] + ";", False),
            ],
            False,
        ),
        (
            ".no-data",
            [
                ("font: 400 20px 'Segoe UI', Ubuntu, Sans-Serif;", False),
                ("fill: " + general_styles[theme]["no_data_color"] + ";", False),
            ],
            False,
        ),
        (
            "@keyframes fadeInAnimation",
            [("from { opacity: 0; } to { opacity: 1; }", True)],
            True,
        ),
    ]

    style = "\n".join(
        [rule[0] + " {" + "\n".join(item[0] for item in rule[1]) + "}" for rule in _style]
    )

    style_no_animation = "\n".join(
        [
            rule[0] + " {" + "\n".join(item[0] for item in rule[1] if not item[1]) + "}"
            for rule in _style
            if not rule[2]
        ]
    )

    return style, style_no_animation









