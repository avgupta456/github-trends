from src.models import UserPackage, WrappedPackage
from src.subscriber.aggregation.wrapped.bar import get_bar_data
from src.subscriber.aggregation.wrapped.calendar import get_calendar_data
from src.subscriber.aggregation.wrapped.numeric import get_numeric_data
from src.subscriber.aggregation.wrapped.pie import get_pie_data

# from src.processing.user.follows import get_user_follows


def main(user_package: UserPackage) -> WrappedPackage:
    """packages all processing steps for the user query"""

    bar_data = get_bar_data(user_package)
    calendar_data = get_calendar_data(user_package)
    numeric_data = get_numeric_data(user_package)
    pie_data = get_pie_data(user_package)

    return WrappedPackage(
        bar_data=bar_data,
        calendar_data=calendar_data,
        numeric_data=numeric_data,
        pie_data=pie_data,
    )
