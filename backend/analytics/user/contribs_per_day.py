from datetime import date
from typing import Dict

from models.user.package import UserPackage


def get_contribs_per_day(data: UserPackage) -> Dict[date, int]:
    contribs_per_day = {x.date: x.stats.contribs_count for x in data.contribs.total}

    print(contribs_per_day)

    return contribs_per_day
