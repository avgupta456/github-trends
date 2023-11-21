from typing import Any

import asyncio
from dotenv import find_dotenv, load_dotenv
from datetime import datetime

load_dotenv(find_dotenv())

# flake8: noqa E402

from src.constants import API_VERSION
from src.data.mongo.main import USER_MONTHS


def get_filters(cutoff_date: datetime) -> Any:
    return {
        "$or": [
            {"month": {"$lte": cutoff_date}},
            {"version": {"$ne": API_VERSION}},
        ],
    }


async def count_old_rows(cutoff_date: datetime) -> int:
    filters = get_filters(cutoff_date)
    num_rows = len(await USER_MONTHS.find(filters).to_list(length=None))  # type: ignore
    return num_rows


async def delete_old_rows(cutoff_date: datetime):
    filters = get_filters(cutoff_date)
    result = await USER_MONTHS.delete_many(filters)
    print(f"Deleted {result.deleted_count} rows")


async def main():
    # Replace 'your_date_field' with the actual name of your date field
    cutoff_date = datetime(2022, 12, 31)

    count = await count_old_rows(cutoff_date)
    if count == 0:
        print("No rows to delete.")
        return

    print(f"Found {count} rows to delete.")
    print()

    confirmation = input("Are you sure you want to delete these rows? (yes/no): ")
    if confirmation.lower() != "yes":
        print("Operation canceled.")
        return

    print()
    await delete_old_rows(cutoff_date)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
