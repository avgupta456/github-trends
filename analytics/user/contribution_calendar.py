from typing import Any, Dict


from models.user.user import UserPackage


def run_month_analysis(data: UserPackage) -> Dict[str, Any]:
    print(data.contribution_calendar.months)
    return {}
