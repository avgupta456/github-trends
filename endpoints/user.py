from typing import Any, Dict

from packaging.user import main as get_data

from analytics.user.contribution_calendar import run_month_analysis


def get_user(user_id: str) -> Dict[str, Any]:
    data = get_data(user_id=user_id)

    month_analysis = run_month_analysis(data)

    return month_analysis
