from typing import Any, Dict, List, Tuple
from datetime import date, datetime

from src.models import ContributionDay, UserPackage


def trim_contribs(
    contribs: List[ContributionDay], start_date: date, end_date: date
) -> Tuple[List[ContributionDay], Dict[str, Any]]:
    new_total = list(
        filter(
            lambda x: datetime.strptime(x.date, "%Y-%m-%d").date() >= start_date
            and datetime.strptime(x.date, "%Y-%m-%d").date() <= end_date,
            contribs,
        )
    )

    new_contribs_count = sum([x.stats.contribs_count for x in new_total])
    new_commits_count = sum([x.stats.commits_count for x in new_total])
    new_issues_count = sum([x.stats.issues_count for x in new_total])
    new_prs_count = sum([x.stats.prs_count for x in new_total])
    new_reviews_count = sum([x.stats.reviews_count for x in new_total])
    new_repos_count = sum([x.stats.repos_count for x in new_total])
    new_other_count = sum([x.stats.other_count for x in new_total])

    new_languages = {}
    for day in new_total:
        for lang in day.stats.languages:
            obj = day.stats.languages[lang]
            if lang not in new_languages:
                new_languages[lang] = {
                    "color": obj.color,
                    "additions": 0,
                    "deletions": 0,
                }
            new_languages[lang]["additions"] += obj.additions
            new_languages[lang]["deletions"] += obj.deletions

    new_total_stats: Dict[str, Any] = {
        "contribs_count": new_contribs_count,
        "commits_count": new_commits_count,
        "issues_count": new_issues_count,
        "prs_count": new_prs_count,
        "reviews_count": new_reviews_count,
        "repos_count": new_repos_count,
        "other_count": new_other_count,
        "languages": new_languages,
    }

    return new_total, new_total_stats


def trim_package(data: UserPackage, start_date: date, end_date: date) -> UserPackage:

    new_total, new_total_stats = trim_contribs(
        data.contribs.total, start_date, end_date
    )

    new_public, new_public_stats = trim_contribs(
        data.contribs.public, start_date, end_date
    )

    new_repos: Dict[str, Any] = {}
    new_repo_stats: Dict[str, Any] = {}
    for repo_name, repo in data.contribs.repos.items():
        new_repo_total, new_repo_total_stats = trim_contribs(repo, start_date, end_date)
        if len(new_repo_total) > 0:
            new_repos[repo_name] = new_repo_total
            new_repo_stats[repo_name] = new_repo_total_stats

    for repo in new_repo_stats:
        new_repo_stats[repo]["private"] = data.contribs.repo_stats[repo].private

    new_data = {
        "total_stats": new_total_stats,
        "public_stats": new_public_stats,
        "total": new_total,
        "public": new_public,
        "repo_stats": new_repo_stats,
        "repos": new_repos,
    }

    return UserPackage.parse_obj({"contribs": new_data})
