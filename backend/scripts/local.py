import argparse
import asyncio
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["LOCAL"] = "True"

# flake8: noqa E402

from src.aggregation.layer0 import get_user_data
from src.processing.user import get_top_languages, get_top_repos
from src.processing.wrapped.package import get_wrapped_data


def parse_args():
    parser = argparse.ArgumentParser(description="GitHub Trends Script")

    parser.add_argument("--user_id", required=True, help="GitHub user ID", type=str)
    parser.add_argument(
        "--access_token", required=True, help="GitHub access token", type=str
    )
    parser.add_argument(
        "--start_date",
        default="2023-01-01",
        help="Start date in YYYY-MM-DD format",
        type=str,
    )
    parser.add_argument(
        "--end_date",
        default="2023-01-31",
        help="End date in YYYY-MM-DD format",
        type=str,
    )
    parser.add_argument(
        "--timezone", default="America/New_York", help="Timezone", type=str
    )
    parser.add_argument(
        "--output_dir", default="./", help="Output directory path", type=str
    )

    return parser.parse_args()


async def main():
    args = parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    print("Local script running...")
    print("User ID:", args.user_id)
    print("Access token:", args.access_token)
    print("Start date:", start_date)
    print("End date:", end_date)
    print("Timezone:", args.timezone)
    print("Output directory:", args.output_dir)
    print()

    raw_output = await get_user_data(
        args.user_id, start_date, end_date, args.timezone, args.access_token
    )

    with open(os.path.join(args.output_dir, "raw.json"), "w") as f:
        f.write(raw_output.model_dump_json(indent=2))

    langs_output = get_top_languages(
        raw_output, loc_metric="changed", include_private=True
    )

    langs_output = (
        [json.loads(x.model_dump_json()) for x in langs_output[0]],
        langs_output[1],
    )

    repos_output = get_top_repos(
        raw_output, loc_metric="changed", include_private=True, group="none"
    )

    repos_output = (
        [json.loads(x.model_dump_json()) for x in repos_output[0]],
        repos_output[1],
    )

    with open(os.path.join(args.output_dir, "langs.json"), "w") as f:
        f.write(json.dumps(langs_output, indent=2))

    with open(os.path.join(args.output_dir, "repos.json"), "w") as f:
        f.write(json.dumps(repos_output, indent=2))

    wrapped_user = get_wrapped_data(raw_output, 2023)

    with open(os.path.join(args.output_dir, "wrapped.json"), "w") as f:
        f.write(wrapped_user.model_dump_json(indent=2))

    print("Wrote output to", args.output_dir)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
