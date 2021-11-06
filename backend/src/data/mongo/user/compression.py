from typing import Any, Dict


def compress_stats(data: Dict[str, Any]) -> Dict[str, Any]:
    out = {
        "counts": (
            data["contribs_count"],
            data["commits_count"],
            data["issues_count"],
            data["prs_count"],
            data["reviews_count"],
            data["repos_count"],
            data["other_count"],
        ),
        "languages": [
            (name, stats["color"], stats["additions"], stats["deletions"])
            for name, stats in data["languages"].items()
        ],
    }

    if "private" in data:
        out["private"] = data["private"]

    return out


def compress(data: Dict[str, Any]) -> Dict[str, Any]:
    new_total_stats = compress_stats(data["contribs"]["total_stats"])
    new_public_stats = compress_stats(data["contribs"]["public_stats"])

    new_total = list(
        map(
            lambda x: {
                "date": x["date"],
                "weekday": x["weekday"],
                "stats": compress_stats(x["stats"]),
            },
            data["contribs"]["total"],
        )
    )

    new_public = list(
        map(
            lambda x: {
                "date": x["date"],
                "weekday": x["weekday"],
                "stats": compress_stats(x["stats"]),
            },
            data["contribs"]["public"],
        )
    )

    new_repo_stats = {
        name: compress_stats(stats)
        for name, stats in data["contribs"]["repo_stats"].items()
    }

    new_repos = {
        repo: list(
            map(
                lambda x: {
                    "date": x["date"],
                    "weekday": x["weekday"],
                    "stats": compress_stats(x["stats"]),
                },
                data["contribs"]["repos"][repo],
            )
        )
        for repo in data["contribs"]["repos"]
    }

    new_data = {
        "contribs": {
            "total_stats": new_total_stats,
            "public_stats": new_public_stats,
            "total": new_total,
            "public": new_public,
            "repo_stats": new_repo_stats,
            "repos": new_repos,
        }
    }

    return new_data


def decompress_stats(data: Dict[str, Any]) -> Dict[str, Any]:
    out = {
        "contribs_count": data["counts"][0],
        "commits_count": data["counts"][1],
        "issues_count": data["counts"][2],
        "prs_count": data["counts"][3],
        "reviews_count": data["counts"][4],
        "repos_count": data["counts"][5],
        "other_count": data["counts"][6],
        "languages": {
            x[0]: {"color": x[1], "additions": x[2], "deletions": x[3]}
            for x in data["languages"]
        },
    }

    if "private" in data:
        out["private"] = data["private"]

    return out


def decompress(data: Dict[str, Any]) -> Dict[str, Any]:
    new_total_stats = decompress_stats(data["contribs"]["total_stats"])
    new_public_stats = decompress_stats(data["contribs"]["public_stats"])

    new_total = list(
        map(
            lambda x: {
                "date": x["date"],
                "weekday": x["weekday"],
                "stats": decompress_stats(x["stats"]),
            },
            data["contribs"]["total"],
        )
    )

    new_public = list(
        map(
            lambda x: {
                "date": x["date"],
                "weekday": x["weekday"],
                "stats": decompress_stats(x["stats"]),
            },
            data["contribs"]["public"],
        )
    )

    new_repo_stats = {
        name: decompress_stats(stats)
        for name, stats in data["contribs"]["repo_stats"].items()
    }

    new_repos = {
        repo: list(
            map(
                lambda x: {
                    "date": x["date"],
                    "weekday": x["weekday"],
                    "stats": decompress_stats(x["stats"]),
                },
                data["contribs"]["repos"][repo],
            )
        )
        for repo in data["contribs"]["repos"]
    }

    new_data = {
        "contribs": {
            "total_stats": new_total_stats,
            "public_stats": new_public_stats,
            "total": new_total,
            "public": new_public,
            "repo_stats": new_repo_stats,
            "repos": new_repos,
        }
    }

    return new_data
