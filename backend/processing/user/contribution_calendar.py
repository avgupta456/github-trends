from models.misc.date import Date, today
from models.user.contribution_calendar import ContributionDay, ContributionCalendar
from external.github_api.graphql.user import (
    get_user_contribution_calendar as run_query,
)


def get_user_contribution_calendar(
    user_id: str,
    start_date: Date = today - 365,
    end_date: Date = today,
) -> ContributionCalendar:
    """get user contributions for the past year"""
    if today - start_date > 365:
        raise AssertionError("start_date can only be within past 1 year")

    try:
        data = run_query(user_id)
    except Exception as e:
        raise e

    contribution_years = data.contribution_years
    total_contributions = data.contribution_calendar.total_contributions
    colors = data.contribution_calendar.colors
    days = list(
        map(
            lambda x: ContributionDay.parse_obj(
                {
                    "date": Date(x.date),
                    "weekday": x.weekday,
                    "contribution_count": x.contribution_count,
                    "contribution_level": x.contribution_level,
                }
            ),
            [
                day
                for week in data.contribution_calendar.weeks
                for day in week.contribution_days
            ],
        )
    )

    calendar = ContributionCalendar(
        contribution_years=contribution_years,
        total_contributions=total_contributions,
        colors=colors,
        days=days,
    )

    return calendar