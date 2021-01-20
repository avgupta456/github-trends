from external.github_api.graphql.user import get_user_contribution_calendar as run_query
from models.misc.date import Date, today
from models.user.contribution_calendar import (
    ContributionCalendar,
    ContributionDay,
    create_contribution_period,
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

    # creates total period (up to 1 year long)
    total = create_contribution_period(days)

    # creates months (0 is January, 11 is December)
    months = [[] for _ in range(12)]
    for day in days:
        months[day.date.month() - 1].append(day)

    months = list(map(lambda x: create_contribution_period(x), months))

    # create weekdays (0 is Sunday, 6 is Saturday)
    weekdays = [[] for _ in range(7)]
    for day in days:
        weekdays[day.weekday].append(day)

    weekdays = list(map(lambda x: create_contribution_period(x), weekdays))

    # create final output
    calendar = ContributionCalendar(
        contribution_years=contribution_years,
        colors=colors,
        total=total,
        months=months,
        weekdays=weekdays,
    )

    return calendar
