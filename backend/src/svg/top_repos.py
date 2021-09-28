# type: ignore

from typing import Any

from svgwrite import Drawing
from svgwrite.container import Group

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


def get_top_repos_svg(data: Any) -> Drawing:
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

    d.add(d.text("Most Contributed Repositories", insert=(25, 35), class_="header"))

    repos = Group(transform="translate(25, 55)")

    if data.top_repos is None:
        raise ValueError("No repository data available")
    data_repos = data.top_repos

    for i in range(min(5, len(data_repos))):
        translate = "translate(0, " + str(40 * i) + ")"
        total = data_repos[0].changed
        repo = Group(transform=translate)
        repo.add(d.text(data_repos[i].repo, insert=(2, 15), class_="lang-name"))
        repo.add(
            d.text(
                format_number(data_repos[i].changed),
                insert=(215, 33),
                class_="lang-name",
            )
        )
        progress = Drawing(width="205", x="0", y="25")
        progress.add(d.rect(size=(205, 8), insert=(0, 0), rx=5, ry=5, fill="#ddd"))
        total_percent = 0
        for j, lang in enumerate(data_repos[i].langs):
            percent, color = 100 * (lang.additions + lang.deletions) / total, lang.color
            box_size, box_insert = (2.05 * percent, 8), (2.05 * total_percent, 0)
            progress.add(
                d.rect(size=box_size, insert=box_insert, rx=5, ry=5, fill=color)
            )

            box_left, box_right = j > 0, j < len(data_repos[i].langs) - 1
            box_size = 2.05 * percent - (0 if box_left else 5) - (0 if box_right else 5)
            box_insert = 2.05 * total_percent + (5 if not box_left else 0)
            progress.add(
                d.rect(size=(max(box_size, 3), 8), insert=(box_insert, 0), fill=color)
            )

            total_percent += percent

        repo.add(progress)
        repos.add(repo)
    d.add(repos)

    return d
