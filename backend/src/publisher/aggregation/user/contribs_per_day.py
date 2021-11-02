from typing import Dict

from src.models.user.package.main import UserPackage


def get_contribs_per_day(data: UserPackage) -> Dict[str, int]:
    contribs_per_day = {x.date: x.stats.contribs_count for x in data.contribs.total}
    return contribs_per_day


def get_contribs_per_repo_per_day(data: UserPackage) -> Dict[str, Dict[str, int]]:
    contribs_per_repo_per_day = {
        name: {x.date: x.stats.contribs_count for x in contrib_days}
        for name, contrib_days in data.contribs.repos.items()
    }
    return contribs_per_repo_per_day
