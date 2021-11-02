from datetime import date, timedelta

from src.subscriber.aggregation.user.package import main as get_data
from src.data.mongo.user.functions import lock_user, update_user_raw_data


async def query_user(user_id: str, access_token: str) -> bool:
    await lock_user(user_id)

    # standard policy is to check past year of data
    start_date = date.today() - timedelta(365)
    end_date = date.today()
    timezone_str = "US/Eastern"

    # TODO: historical data is never updated,
    # don't query full history each time, instead
    # define function to build on previous results

    # TODO: improve performance to store > 1 year
    # ideally five years, leads to issues currently

    output = await get_data(user_id, access_token, start_date, end_date, timezone_str)

    await update_user_raw_data(user_id, output)

    return True
