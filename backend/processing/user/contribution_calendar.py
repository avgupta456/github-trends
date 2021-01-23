from external.github_api.graphql.user import get_user_contribution_calendar as run_query
from models.misc.date import Date, today
from models.user.contribution_calendar import (
    UserContribCalendar,
    ContributionDay,
    create_contribution_period,
)


def get_user_contribution_calendar(
    user_id: str,
    start_date: Date = today - 365,
    end_date: Date = today,
) -> UserContribCalendar:
    """get user contributions for the past year"""
    if today - start_date > 365:
        raise AssertionError("start_date can only be within past 1 year")

    data = run_query(user_id)

    contribution_years = data.contribution_years
    colors = data.contribution_calendar.colors
    days = map(
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

    days = list(filter(lambda x: start_date <= x.date <= end_date, days))

    # creates total period (up to 1 year long)
    total = create_contribution_period(days)

    # creates months (0 is first month, up to present)
    start_year, start_month = start_date.year(), start_date.month()
    year_diff = end_date.year() - start_year
    month_diff = end_date.month() - start_month
    num_months = year_diff * 12 + month_diff + 1
    months = [[] for _ in range(num_months)]
    for day in days:
        date = day.date
        year_diff = date.year() - start_year
        month_diff = date.month() - start_month
        index = year_diff * 12 + month_diff
        months[index].append(day)

    months = list(map(lambda x: create_contribution_period(x), months))

    # create weekdays (0 is Sunday, 6 is Saturday)
    weekdays = [[] for _ in range(7)]
    for day in days:
        weekdays[day.weekday].append(day)

    weekdays = list(map(lambda x: create_contribution_period(x), weekdays))

    # create final output
    calendar = UserContribCalendar(
        contribution_years=contribution_years,
        colors=colors,
        total=total,
        months=months,
        weekdays=weekdays,
    )

    return calendar
