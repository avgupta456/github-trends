from typing import Any, Dict, List, Tuple, Union
from datetime import date, datetime, timedelta

from src.models.user.contribs import ContributionDay, RepoContributionDay
from src.models.user.package import UserPackage


def trim_contribs(
    contribs: Union[List[ContributionDay], List[RepoContributionDay]],
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
) -> Tuple[List[Union[ContributionDay, RepoContributionDay]], Dict[str, Any]]:
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


def trim_package(
    data: UserPackage,
    start_date: date = date.today() - timedelta(365),
    end_date: date = date.today(),
) -> UserPackage:

    new_total, new_total_stats = trim_contribs(data.contribs.total)

    new_repos = {}
    new_repo_stats = {}
    for repo_name, repo in data.contribs.repos.items():
        new_repo_total, new_repo_total_stats = trim_contribs(repo)
        if len(new_repo_total) > 0:
            new_repos[repo_name] = new_repo_total
            new_repo_stats[repo_name] = new_repo_total_stats

    new_data = {
        "total_stats": new_total_stats,
        "total": new_total,
        "repo_stats": new_repo_stats,
        "repos": new_repos,
    }

    return UserPackage.parse_obj({"contribs": new_data})
