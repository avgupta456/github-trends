from typing import List, Tuple, Dict

# List[Tuple["selector", List[Tuple["property", "is_animation"]], "is_animation"]]

_style: List[Tuple[str, List[Tuple[str, bool]], bool]] = [
    (
        ".header",
        [
            ("font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;", False),
            ("fill: #2f80ed;", False),
            ("animation: fadeInAnimation 0.8s ease-in-out forwards;", True),
        ],
        False,
    ),
    (
        ".subheader",
        [
            ("font: 500 10px 'Segoe UI', Ubuntu, San-Serif;", False),
            ("fill: #666;", False),
            ("animation: fadeInAnimation 0.8s ease-in-out forwards;", True),
        ],
        False,
    ),
    (
        ".lang-name",
        [
            ("font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif;", False),
            ("fill: #333", False),
        ],
        False,
    ),
    (
        ".no-data",
        [
            ("font: 400 20px 'Segoe UI', Ubuntu, Sans-Serif;", False),
            ("fill: #777;", False),
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

background_styles: Dict[str, Dict[str, str]] = {
    "classic": {
        "main_fill_color": "#e4e2e2",
        "border_color": "#fffefe",
        "bar_default_color": "#ddd",
    },
    "dark": {
        "main_fill_color": "#1F1F1F",
        "border_color": "#7B8794",
        "bar_default_color": "#333333",
    }
}
