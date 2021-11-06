from datetime import date, timedelta
import requests

from src.subscriber.aggregation import get_data
from src.data.mongo.user import lock_user, update_user_raw_data
from src.constants import BACKEND_URL, DOCKER, LOCAL_PUBLISHER, PROD
from src.utils.alru_cache import alru_cache


s = requests.Session()


@alru_cache()
async def query_user(user_id: str, access_token: str) -> bool:
    await lock_user(user_id)

    # standard policy is to check past year of data
    start_date = date.today() - timedelta(365)
    end_date = date.today()
    timezone_str = "US/Eastern"

    # TODO: if a user just signed up, sometimes GitHub
    # hasn't updated their access token immediately
    # Not a major problem because querying on website
    # will re-trigger this function

    # TODO: historical data is never updated,
    # don't query full history each time, instead
    # define function to build on previous results

    # TODO: improve performance to store > 1 year
    # ideally five years, leads to issues currently

    output = await get_data(user_id, access_token, start_date, end_date, timezone_str)

    await update_user_raw_data(user_id, output)

    # cache buster for publisher
    if PROD:
        s.get(BACKEND_URL + "/user/db/get/metadata/" + user_id + "?no_cache=True")
        s.get(BACKEND_URL + "/user/db/get/" + user_id + "?no_cache=True")
    elif DOCKER:
        s.get(LOCAL_PUBLISHER + "/user/db/get/metadata/" + user_id + "?no_cache=True")
        s.get(LOCAL_PUBLISHER + "/user/db/get/" + user_id + "?no_cache=True")

    return (True, True)  # type: ignore
