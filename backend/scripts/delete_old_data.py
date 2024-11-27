import asyncio
import os
import sys
from datetime import datetime
from typing import Any

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    cutoff_date = datetime(2024, 12, 31)

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
